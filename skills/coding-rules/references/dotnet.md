# C# / .NET

A starter. The cross-language body holds most of what matters; the .NET rules below grow as repos teach them. Expand from real code, do not pad.

The creed under the bans is the one Go, Rust, and Zig share: cost and control flow must be visible at the call site. C# hides both behind clean syntax. The list drags it back into the open, and it fails the build, not review (see Enforcement).

Targets .NET 10. Native `union` types (C# 15 / .NET 11) replace the Result emulation below once they reach GA; do not gate this skill on the preview SDK.

## Defaults

- Data-oriented. Plain data plus functions, not behaviour-bearing objects that hide mutable state.
- Public fields, not properties. A field is honest: it reads and writes, nothing else. `readonly` by default so data is immutable after construction (Rust's `let`); drop `readonly` only where mutation is the point.
- `record` types for carried data, declared with public fields in the body, not positional parameters (positional members compile to properties). You keep field-based value equality and `ToString` and lose nothing but the hidden accessors.
- Construct fully formed through a real constructor. The ctor is the completeness check: a half-built object cannot exist. Call it with named arguments for readability (`new Money(amount: 100, currency: "AUD")`). No `{...}` object initializers (they do not enforce completeness), no builder pattern (build-it-up-across-calls is the temporal coupling the body bans). Immutable update is an explicit reconstruction; C# has no `..spread` for ctors, so there is no `with` sugar here, and that is the accepted cost of honest fields.
- Errors are values, not thrown exceptions, for anything expected or recoverable. Common case: a hand-rolled `Result<T,E>` (`readonly struct` with `Match(ok, err)` that forces the caller to handle both arms). Multi-shape failures: a closed `sealed record` hierarchy matched by a switch expression. Be honest about the .NET 10 limit: the compiler cannot prove a record hierarchy closed, so a `_ => Panic(...)` arm is a runtime guard, not a compile-time check. A new variant compiles clean and routes to `Panic` at runtime; it does not fail the build. Real compile-time exhaustiveness holds only for `enum`/closed switches (CS8509-as-error, no discard arm) until native `union` (C# 15) extends it to hierarchies.
- Minimal state in services. Stateless services that take what they need and return a result.
- Idempotency on retryable writes: an idempotency key plus a client sequence number so a retry is safe, part of the contract, not an afterthought.
- Dependency injection for the composition DAG. Constructor injection only, registrations written out explicitly at one composition root, `Microsoft.Extensions.DependencyInjection`. Transient or singleton lifetimes only, never scoped. DI wires the graph; it does not run magic.
- LINQ is fine, and good. Declarative transforms over data are the whole point of data-oriented code. The only caution is the hot path, where deferred execution and allocation cost; there, see `performance-discipline`.

## Sum types (closed unions)

Rust models "one of N shapes" with an `enum`, and `match` proves every arm is handled. C# has no algebraic enum until native `union` (C# 15). Until then, model a sum type as a closed `sealed record` hierarchy: an abstract base with a **private** constructor, variants nested inside it. The private ctor is the closure; only nested types can reach it, so nothing outside the file can add a variant.

```csharp
public abstract record Shape
{
    private Shape() { }                 // closes the set: only nested variants can derive

    public sealed record Circle : Shape
    {
        public readonly double Radius;
        public Circle(double radius) => Radius = radius;
    }

    public sealed record Rectangle : Shape
    {
        public readonly double Width;
        public readonly double Height;
        public Rectangle(double width, double height) => (Width, Height) = (width, height);
    }
}
```

Match with a switch expression, one arm per variant, `_ => Panic(...)` last:

```csharp
double Area(Shape shape) => shape switch
{
    Shape.Circle c    => Math.PI * c.Radius * c.Radius,
    Shape.Rectangle r => r.Width * r.Height,
    _                 => Panic($"unhandled Shape variant: {shape}"),
};
```

This is data-modeling inheritance, variants of a closed set with no behaviour inherited, not the implementation inheritance banned below. The base ships no methods to override; the switch holds the behaviour, so adding an operation is a new switch, not a new virtual.

Two shape rules, non-negotiable:

- **The base holds no fields.** It is a pure tag. All data lives on the variants, never hoisted to the top level "because every variant has it"; a shared field on the base is data inheritance creeping back in. If two variants share a field, that is a coincidence to repeat, not a base to extract.
- **One level deep.** Variants are the leaves. No variant is itself an abstract base with its own nested variants. A union of unions defeats the closure and the switch (you now match a tree, not a set). If a variant needs sub-cases, make it a separate closed union held as a field and switch on it separately.

Two honest costs:

- **Not compile-time exhaustive.** .NET 10 will not prove the hierarchy closed even with the private ctor, so a new variant compiles clean and routes to `Panic` at runtime. The `_` arm is a guard, not a proof. Only `enum`/closed switches get CS8509; native `union` closes the gap.
- **Verbose variants.** The property ban forces body fields over positional records, so each variant carries its own ctor boilerplate. The accepted cost until `union` lands.

## Value types and the stack

A C# struct is not a Rust struct. Rust's move is O(1) at any size; C#'s struct copy is O(size). Move lets Rust use `struct` as both the modeling primitive and the performance primitive. Copy caps C# structs at small, so the jobs split: reference types model the domain, value types are a performance tool for leaf data. Do not reach for structs to "be like Rust"; you get stack locality and value semantics, none of the ownership safety, and copy and boxing footguns Rust does not have.

- A struct copies on every assignment, return, and argument pass. There is no move and no ownership; the borrow checker, `Drop`, and lifetimes have no general analog. `ref struct` + `scoped` (stack-only, ref-safety) is the one Rust-like corner, confined to spans.
- Two good uses, both avoid the copy. First: small immutable values passed by value (Vec3, Money, id wrappers), up to ~24 bytes, 2-3 machine words. Second: elements of a contiguous array or `Span<T>` touched by `ref` (one flat cache-friendly block, no per-element heap object). The data-oriented hot path is the second.
- Poison: a mid or large struct passed by value through a call chain. Every hop memcpys it, slower than the class it was avoiding. If a struct must be big and cross signatures, thread `in` / `ref readonly`, but that is manual plumbing and one forgotten `in` silently copies again.
- A struct always has a zero `default` that bypasses constructors (`new T[n]` gives n of them), so it cannot enforce a non-default invariant. When an invariant must hold, use a `sealed class` / `record class`.
- Map intent, not the keyword: Rust `Copy` newtype to `readonly struct`; owned struct with identity or invariants to `sealed class` / `record class`; `&[T]` to `Span<T>` / `ReadOnlySpan<T>`; `enum` to `union` / sealed records; `&T` / `&mut T` to `in T` / `ref T`. Default struct equality boxes, and falls back to reflection once the struct holds reference-type fields, so implement `IEquatable<T>` or use `record struct`.

## Performance is a one-way door

`performance-discipline` owns the measurement loop and the generic cost choices; do not guess, benchmark. This section is the .NET-specific part, and it leads with the decisions you cannot cheaply reverse. A slow method body is a later fix the profiler points at. The allocation model, async coloring, data layout, and AOT-compatibility are load-bearing: they shape every signature built on top, so decide them at design time with the cost model in hand, not in an optimisation pass that never comes.

- **Allocation model.** GC pressure dominates .NET throughput and tail latency. "Allocate per item or per request" versus "pool and reuse" is baked into your types and signatures (`new List<T>` and arrays versus `Span<T>` and pooled buffers), and retrofitting it rewrites the API. On a hot path: `Span<T>` / `ReadOnlySpan<T>`, `stackalloc` for small transient buffers, `ArrayPool<T>.Shared` for larger, buffers reused across calls.
- **Async coloring.** `async` is viral. It colours every caller and each `Task<T>` is a heap-allocated state machine. Going async is a one-way door up the call stack, so decide sync versus async at the boundary deliberately, not by reflex. `ValueTask<T>` for hot paths that usually complete synchronously; `IAsyncEnumerable<T>` for streaming.
- **Data layout.** Hot data wants to be contiguous: a value-type array the CPU streams through (`Particle[]`, struct-of-arrays), not an array of heap objects scattered across the heap. Locality is a type-shape decision; you cannot fix it without changing the type. See the value-types section.
- **Boxing.** A struct behind an interface or an unconstrained generic boxes and allocates silently. `where T : struct` constraints, concrete collection types, and struct enumerators keep hot loops allocation-free.
- **Strings.** Interpolation, concat, and `Substring` allocate. On hot paths use `ReadOnlySpan<char>` slicing, `string.Create`, and the interpolated-string handler, not naive `+`.
- **AOT-compatibility.** If the target is Native AOT (single static binary, fast startup, no JIT), reflection, `dynamic`, and runtime codegen are out. They are already banned, so the bans double as a startup-and-AOT decision; an AOT-hostile dependency chosen early is the expensive mistake.

Enforcement here is opt-in per project, not global: add a heap-allocation analyzer to the genuinely hot assemblies only. You cannot ban allocation across a codebase, and pretending you can just trains people to suppress.

## Concurrency and locking

.NET's default is a shared, work-stealing thread pool: async continuations hop pool threads and state is shared by reflex. That is the opposite of the thread-per-core model in `rust.md` (state owned by a core, no shared lock, message-pass). Do not carry assumptions between them. In a thread-pool app the locking discipline is its own one-way door, and most lock bugs are really shared-state bugs.

Order of preference, lock last:

1. **No shared mutable state.** Immutable readonly-field data and stateless services (the defaults above) need no lock. A lock on a hot path means the data is shared when it should not be, the same tell as `Arc<Mutex>` on thread-per-core.
2. **Message-pass.** `System.Threading.Channels.Channel<T>` for producer-consumer instead of shared state plus a lock. The thread-pool analog of passing work across cores.
3. **Lock-free for the simple cases.** `Interlocked` for counters, `ConcurrentDictionary` for a shared cache.
4. **Only then a lock,** for genuinely shared mutable state off the hot path. Use the C# 13 `System.Threading.Lock` type, not `lock(object)`. Hold it briefly, never around I/O.

The hard rules, because the work-stealing pool punishes both:

- **Never hold a lock across an `await`.** A thread-affine lock (`lock` / `Monitor`) must release on the acquiring thread, but the continuation resumes on another. C# blocks `await` inside `lock` (CS1996); the trap is the lookalike, a `SemaphoreSlim` held across an await, which is almost always shared state that should not be shared. The async-safe mutual exclusion is `SemaphoreSlim(1,1)` with `WaitAsync`, and reaching for it is a smell.
- **Never block a pool thread.** `.Result`, `.Wait()`, `.GetAwaiter().GetResult()`, and lock contention block a work-stealing worker. The pool grows by slow hill-climbing, so blocked workers starve it, the classic sync-over-async deadlock. Async all the way to the boundary; no sync-over-async.

*Enforced: `Microsoft.VisualStudio.Threading.Analyzers` (VSTHRD002 sync-over-async, VSTHRD110 unobserved async result, VSTHRD100 async void) at error. Skip VSTHRD012, it is specific to the VS JoinableTaskFactory model we do not use.*

## Restraint

- Lean on the standard library and plain composition before AOP, source generators, or a mediator stack. Magic that hides the call graph is hard to reason about and hard to test in the dark. DI is the one allowed framework, and only in its explicit-wiring subset.

## Banned until argued otherwise

Compiler- or CI-enforced where the note says so.

- **Properties. All of them.** Public fields only. `obj.Foo` that looks like a field but runs code (allocates, throws, does I/O via an EF lazy-loaded nav property, runs O(n)) is the exact hidden-cost lie Go, Rust, and Zig refuse. A field cannot lie. A computation is a method, and the parens are the honesty. Record body fields are fields, so they are fine; positional-record properties are not. *Enforced: custom analyzer, error.*
- **Thrown exceptions as an error channel.** Expected and recoverable failures return `Result<T,E>`. At a framework boundary catch what the platform throws and convert it; do not let throwing propagate into our code. Carve-out, the `panic!()` equivalent: genuinely unrecoverable invariant violations call `Environment.FailFast` (immediate abort, no unwinding, nothing catches it, which is `panic = "abort"`), never a throw-and-pray. *Enforced: custom analyzer bans `throw` outside the `Panic` helper, error.*
- **`implicit operator`.** A hidden function call on what looks like an assignment. `explicit` is tolerable; the cast is visible. Zig bans implicit casts outright for the same reason. *Enforced: custom analyzer, error.*
- **`async void`.** Uncatchable, unawaitable, no failure channel; an exception inside tears down the process. Wrap even the event-handler case. *Enforced: VSTHRD100 / Roslynator, error.*
- **The null-forgiving `!`.** NRT on, warnings as errors. Each `!` is a place you told the compiler to stop helping. Unwrap the absence; do not paper over it. *Enforced: `<Nullable>enable</Nullable>` + warnings-as-errors.*
- **`switch` with a swallowing `default:`.** On an `enum` or closed set, omit the discard so CS8509-as-error flags a missing case (Rust's `match`, the cheapest correctness win). On a `sealed record` hierarchy .NET 10 cannot prove closure, so the lone `_ => Panic(...)` arm stays as a runtime guard; do not mistake it for compile-time exhaustiveness. A swallowing `default:` that returns or continues, hiding the unhandled case, is the banned shape. *Enforced: CS8509 as error for enum/closed switches; native `union` extends it to hierarchies later.*
- **Open-by-default classes and implementation inheritance.** `sealed` is the default; open a type deliberately. `protected` hierarchies hide where behaviour comes from. Compose, depend on small interfaces. Go and Rust ship without inheritance and are fine. *Enforced: custom analyzer / NetArchTest, error.*
- **Mutable structs.** A struct is `readonly`. Copy-on-assign means a mutation through a `foreach` variable, a collection slot, or any copy lands on a copy and vanishes silently. Mutate array or span elements by `ref`, never a loose struct copy. *Enforced: IDE0250 as error.*
- **DI container magic.** Inside the allowed DI: no assembly-scanning or convention auto-registration, no `[Inject]`/attribute or property injection, no service-locator (`IServiceProvider.GetService` sprinkled through code), no MediatR-style runtime dispatch. Wire it explicitly or not at all. *Enforced: BannedApiAnalyzers, error.*
- **`dynamic`.** Throws the type system away, moves errors to runtime, buys nothing in the code we write. *Enforced: custom analyzer, error.*
- **Reflection-and-attribute magic that hides what actually runs.** *Enforced: BannedApiAnalyzers on the `System.Reflection` hot spots, error.*

## Enforcement

The bans fail the build, not review. Reuse what exists, write only the rules nobody ships. All inherited per-repo from `Directory.Build.props`:

- **Reused analyzers** carry most of it: `Meziantou.Analyzer` (MA0053 flags classes that can be sealed; turn on its public-class option, it only sees same-assembly subtypes), `Apex.Analyzers` (`[Immutable]`: fields readonly, no setters, member types immutable), `ErrorProne.NET` (exception/correctness), `Microsoft.VisualStudio.Threading.Analyzers` (sync-over-async, lock-across-await, async void), `Microsoft.CodeAnalysis.BannedApiAnalyzers` with a `BannedSymbols.txt` for the API-shaped bans (reflection entry points, `IServiceProvider.GetService`).
- **The custom analyzer** is only the four nobody ships, because they are unusually strict: property declarations, `throw` outside the `Panic` helper, `implicit operator`, `dynamic`. Each is one syntax-node rule emitting `DiagnosticSeverity.Error`, so `dotnet build` fails. The property rule ships a CodeFix (property to `public readonly` field) so `dotnet format analyzers` auto-applies it.
- **`.editorconfig`** sets severity `error` on the built-in IDs: nullable (CS86xx), exhaustiveness (CS8509), and struct hygiene (`IDE0250` struct readonly, `IDE0251` member readonly, `CA1815` equality on value types).
- **`<EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>`** is required or the `IDE*` rules (IDE0250/IDE0251) only light up in the editor and never fail `dotnet build`. `CA*` rules (CA1815) run without it.
- **Disable the platform rules that fight the bans.** The default analyzers stay quiet, but a repo that raises `<AnalysisMode>` turns on Microsoft rules that contradict this style: `CA1051` (use properties, not public fields) fights HON001, `CA1034` (no nested types) forbids the nested-record sum types, `CA1062` (its fix is a `throw`) fights HON002. Set those three to `none` so they cannot fire whatever the consumer's analysis mode. Turn on the ones that agree: `IDE0044` (readonly fields), and `CA1852` (seal internal types) where MA0053 does not already cover it.
- **`<TreatWarningsAsErrors>true</TreatWarningsAsErrors>`** so nothing downgrades silently.
- **One gate command.** `check.sh` runs `dotnet build` then `dotnet test` (NetArchTest fixtures for whole-assembly rules). CI and the agent run that one script. If it compiles and tests pass, it is in policy.
