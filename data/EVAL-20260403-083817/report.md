# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260403-083817
**Timestamp:** 2026-04-03T08:38:17.958725
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

Create TypeScript types that enforce these compile-time constraints:

1. A `Route` type where the path parameters in the URL template must match the params object:
   - `createRoute('/users/:userId/posts/:postId', { userId: '123', postId: '456' })` ✓
   - `createRoute('/users/:userId', { wrongParam: '123' })` ✗ (compile error)

2. A `Builder` pattern type where methods can only be called in a specific order:
   - `builder.setName('x').setAge(25).build()` ✓
   - `builder.setAge(25).setName('x').build()` ✗ (compile error)
   - `builder.setName('x').build()` ✗ (compile error - age not set)

Show the type definitions and example usage.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-5.4 | 9.12 | 8.80 | 9.80 | 0.41 |
| 2 | Gemini 3 Flash Preview | 9.03 | 8.00 | 10.00 | 0.62 |
| 3 | Claude Sonnet 4.6 | 8.85 | 8.00 | 10.00 | 0.61 |
| 4 | GPT-OSS-120B | 8.57 | 7.25 | 9.80 | 0.86 |
| 5 | Claude Opus 4.6 | 8.52 | 6.05 | 9.80 | 1.07 |
| 6 | MiMo-V2-Flash | 8.11 | 6.80 | 9.80 | 1.08 |
| 7 | Grok 4.20 | 7.77 | 5.80 | 9.60 | 1.21 |
| 8 | DeepSeek V3 | 7.67 | 6.75 | 9.55 | 0.87 |
| 9 | Gemini 3.1 Pro | 1.62 | 0.45 | 3.00 | 0.85 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 6.38 |
| 2 | Claude Opus 4.6 | 7.05 |
| 3 | Claude Sonnet 4.6 | 7.26 |
| 4 | Grok 4.20 | 7.33 |
| 5 | GPT-OSS-120B | 7.62 |
| 6 | MiniMax M2.5 | 7.69 |
| 7 | MiMo-V2-Flash | 8.12 |
| 8 | Gemini 3.1 Pro | 8.18 |
| 9 | DeepSeek V3 | 8.51 |
| 10 | Gemini 3 Flash Preview | 8.80 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** gemini_3_flash
**Total Judgments:** 100
**Valid Judgments:** 81

---

## Model Pool

Models selected for **Code Generation** evaluation:

1. **GPT-5.4** (openrouter)
2. **Claude Opus 4.6** (openrouter)
3. **Gemini 3.1 Pro** (openrouter)
4. **Claude Sonnet 4.6** (openrouter)
5. **Grok 4.20** (openrouter)
6. **DeepSeek V3** (openrouter)
7. **GPT-OSS-120B** (openrouter)
8. **Gemini 3 Flash Preview** (openrouter)
9. **MiniMax M2.5** (openrouter)
10. **MiMo-V2-Flash** (openrouter)

---

## Model Responses

### GPT-5.4

**Generation Time:** 14321ms
**Tokens:** 1000

```
```ts
// =========================
// 1. Route param checking
// =========================

// Extract `:param` names from a route string
type ExtractRouteParams<Path extends string> =
  Path extends `${string}:${infer Param}/${infer Rest}`
    ? Param | ExtractRouteParams<`/${Rest}`>
    : Path extends `${string}:${infer Param}`
      ? Param
      : never;

// Build the required params object type from the path
type RouteParams<Path extends string> = {
  [K in ExtractRouteParams<Path>]: string;
};

// Optional: forbid extra keys as well
type Exact<TExpected, TActual extends TExpected> =
  TExpected & Record<Exclude<keyof TActual, keyof TExpected>, never>;

// Route creator
function createRoute<
  Path extends string,
  Params extends RouteParams<Path>
>(
  path: Path,
  params: Exact<RouteParams<Path>, Params>
) {
  return { path, params };
}

// ✅ OK
const r1 = createRoute('/users/:userId/posts/:postId', {
  userId: '123',
  postId: '456',
});

// ❌ Compile error: wrongParam does not match :userId
const r2 = createRoute('/users/:userId', {
  wrongParam: '123',
});

// ❌ Compile error: missing postId
const r3 = createRoute('/users/:userId/posts/:postId', {
  userId: '123',
});

// ❌ Compile error: extra key not allowed
const r4 = createRoute('/users/:userId', {
  userId: '123',
  extra: 'nope',
});


// =========================
// 2. Ordered Builder pattern
// =========================

type BuiltPerson = {
  name: string;
  age: number;
};

type NameStage = {
  setName(name: string): AgeStage;
};

type AgeStage = {
  setAge(age: number): BuildStage;
};

type BuildStage = {
  build(): BuiltPerson;
};

// Runtime implementation can satisfy all stages,
// but exposed type controls call order.
function createBuilder(): NameStage {
  const state: Partial<BuiltPerson> = {};

  const api = {
    setName(name: string) {
      state.name = name;
      return api;
    },
    setAge(age: number) {
      state.age = age;
      return api;
    },
    build() {
      return s...
```

### Claude Opus 4.6

**Generation Time:** 268209ms
**Tokens:** 2254

```


# Compile-Time Constraint Types in TypeScript

## 1. Type-Safe Route Parameters

```typescript
// ============================================================
// ROUTE PARAMETER EXTRACTION & ENFORCEMENT
// ============================================================

/**
 * Extracts parameter names from a URL template string.
 * "/users/:userId/posts/:postId" → "userId" | "postId"
 */
type ExtractRouteParams<T extends string> =
  // Match segments that start with ":"
  T extends `${infer _Start}:${infer Param}/${infer Rest}`
    ? Param | ExtractRouteParams<Rest>
    : T extends `${infer _Start}:${infer Param}`
      ? Param
      : never;

/**
 * Builds the required params object type from extracted parameter names.
 * "userId" | "postId" → { userId: string; postId: string }
 */
type RouteParams<T extends string> = {
  [K in ExtractRouteParams<T>]: string;
};

/**
 * The Route type carries its template and parsed params.
 */
interface Route<T extends string> {
  readonly template: T;
  readonly params: RouteParams<T>;
  /** Produces the resolved URL with params substituted */
  readonly url: string;
}

/**
 * Creates a type-safe route. The params object MUST contain exactly
 * the parameters declared in the URL template — no more, no less.
 *
 * The `& Record<string, never>` trick on Exclude ensures that
 * extra keys cause a compile error via the Exact constraint.
 */
type ExactRouteParams<T extends string, P> =
  P extends RouteParams<T>
    ? Exclude<keyof P, ExtractRouteParams<T>> extends never
      ? P
      : never
    : never;

function createRoute<
  T extends string,
  P extends RouteParams<T>
>(
  template: T,
  // Enforce exact match: no missing keys, no extra keys
  ...args: ExactRouteParams<T, P> extends never
    ? [params: P & `ERROR: params must exactly match route parameters`]
    : [params: P]
): Route<T> {
  const params = args[0] as RouteParams<T>;
  let url: string = template;
  for (const [key, value] of Object.entries(params)) {
    url = ...
```

### Gemini 3.1 Pro

**Generation Time:** 30774ms
**Tokens:** 2233

```
never`. Total: `'x'`. Works perfectly.
    *   *Builder:* Is it possible to implement this cleanly in a class so it's not just types?
        *   Yes, a single class can implement all interfaces.
        ```typescript
        class UserBuilder implements NameBuilder, AgeBuilder, FinalBuilder {
            private name!: string;
            private age
```

### Claude Sonnet 4.6

**Generation Time:** 32775ms
**Tokens:** 2254

```
# TypeScript Compile-Time Constraint Types

## Part 1: Route Path Parameter Extraction

```typescript
// ============================================================
// UTILITY TYPES: Extract parameter names from URL templates
// ============================================================

/**
 * Extracts parameter names from a path template string.
 * '/users/:userId/posts/:postId' → 'userId' | 'postId'
 *
 * Works by recursively splitting on ':' and extracting
 * the segment before the next '/' or end of string.
 */
type ExtractRouteParams<Path extends string> =
  // Does the path contain a colon? If so, process it.
  Path extends `${string}:${infer Param}/${infer Rest}`
    ? Param | ExtractRouteParams<`/${Rest}`>  // param before '/', recurse on rest
    : Path extends `${string}:${infer Param}`
    ? Param                                    // param at end of string
    : never;                                   // no more params

/**
 * Converts extracted param names into a required params object type.
 * 'userId' | 'postId' → { userId: string; postId: string }
 */
type RouteParams<Path extends string> = {
  [K in ExtractRouteParams<Path>]: string;
};

// ============================================================
// ROUTE FUNCTION
// ============================================================

/**
 * The params argument type is derived from the path template.
 * TypeScript will enforce that EXACTLY the right params are provided.
 *
 * The conditional type on Params ensures:
 * - If no params exist in path → params must be Record<never, never> (empty)
 * - If params exist → params must match exactly
 */
function createRoute<Path extends string>(
  path: Path,
  // RouteParams<Path> will be Record<never,never> when no params exist
  params: ExtractRouteParams<Path> extends never
    ? Record<never, never>
    : RouteParams<Path>
): { path: Path; params: typeof params; resolved: string } {
  // Replace each :param with its value at runtime
  const resolved = ...
```

### Grok 4.20

**Generation Time:** 7804ms
**Tokens:** 1771

```
**Solution:** TypeScript types with compile-time enforcement

### 1. Route Type with Path Parameter Matching

```ts
type ExtractParams<T extends string> =
  T extends `${string}:${infer Param}/${infer Rest}`
    ? Param | ExtractParams<`/${Rest}`>
    : T extends `${string}:${infer Param}`
      ? Param
      : never;

type ParamsObject<T extends string> = {
  [K in ExtractParams<T>]: string | number;
};

type RouteFn = <T extends string>(
  path: T,
  params: ParamsObject<T>
) => string;

const createRoute: RouteFn = (path, params) => {
  return Object.entries(params).reduce((acc, [key, value]) => {
    return acc.replace(`:${key}`, String(value));
  }, path);
};

// ✅ Valid usages
createRoute('/users/:userId/posts/:postId', { 
  userId: '123', 
  postId: '456' 
});

createRoute('/users/:userId', { 
  userId: '123' 
});

// ❌ Compile errors:
createRoute('/users/:userId', { wrongParam: '123' }); // Missing userId + extra param
createRoute('/users/:userId/posts/:postId', { userId: '123' }); // Missing postId
```

### 2. Builder Pattern with Strict Call Order

```ts
// State tracking using branded types
type RequiredFields = 'name' | 'age';

type BuilderState = {
  name: boolean;
  age: boolean;
};

type SetField<T extends keyof BuilderState> = 
  BuilderState & { [K in T]: true };

class Builder {
  private state: BuilderState = {
    name: false,
    age: false,
  };

  private data: { name?: string; age?: number } = {};

  setName(name: string): BuilderAfterSet<'name'> {
    this.data.name = name;
    this.state.name = true;
    return this as any;
  }

  setAge(age: number): BuilderAfterSet<'age'> {
    this.data.age = age;
    this.state.age = true;
    return this as any;
  }

  build(): { name: string; age: number } {
    if (!this.state.name || !this.state.age) {
      throw new Error('All fields must be set');
    }
    return this.data as { name: string; age: number };
  }
}

// Helper type to track what has been set
class BuilderAfterSet<T extends keyof Bui...
```

### DeepSeek V3

**Generation Time:** 29274ms
**Tokens:** 1126

```
# TypeScript Types for Enforcing Compile-Time Constraints

Here are TypeScript type definitions that enforce the constraints you described:

## 1. Route with Path Parameter Validation

```typescript
type ExtractRouteParams<T extends string> = 
    T extends `${infer _}:${infer Param}/${infer Rest}` 
    ? Param | ExtractRouteParams<`${Rest}`> 
    : T extends `${infer _}:${infer Param}` 
    ? Param 
    : never;

type ValidateRouteParams<Path extends string, Params extends Record<string, string>> = 
    ExtractRouteParams<Path> extends keyof Params 
    ? (Params extends Record<ExtractRouteParams<Path>, string> 
        ? Path 
        : never)
    : never;

function createRoute<Path extends string, Params extends Record<string, string>>(
    path: ValidateRouteParams<Path, Params>,
    params: Params
): string {
    let result = path as string;
    for (const [key, value] of Object.entries(params)) {
        result = result.replace(`:${key}`, value);
    }
    return result;
}

// Example usage:
const validRoute = createRoute('/users/:userId/posts/:postId', { userId: '123', postId: '456' }); // OK

// These would cause compile errors:
// const invalidRoute1 = createRoute('/users/:userId', { wrongParam: '123' }); // Error
// const invalidRoute2 = createRoute('/users/:userId', {}); // Error
```

## 2. Builder Pattern with Ordered Method Chaining

```typescript
interface EmptyBuilder {
    setName(name: string): NameBuilder;
}

interface NameBuilder {
    setAge(age: number): ReadyBuilder;
}

interface ReadyBuilder {
    build(): Person;
}

interface Person {
    name: string;
    age: number;
}

class PersonBuilder implements EmptyBuilder {
    private name?: string;
    private age?: number;

    setName(name: string): NameBuilder {
        this.name = name;
        return this as unknown as NameBuilder;
    }

    setAge(age: number): ReadyBuilder {
        this.age = age;
        return this as unknown as ReadyBuilder;
    }

    build(): Person {
        if (!th...
```

### GPT-OSS-120B

**Generation Time:** 11590ms
**Tokens:** 2280

```
Below are two independent, **pure‑type** solutions – no runtime magic is required.  
All the checks are done by the TypeScript compiler, so the examples that are marked
with **✗** will not compile.

---

## 1️⃣ `Route` – URL‑template → params object must match exactly

### 1.1  Extract the parameter names from a string literal

```ts
// Recursively walk through the template and collect every ":param"
type ExtractParams<S extends string> =
    //   head   :   param   /   tail
    S extends `${infer _Start}:${infer Param}/${infer Rest}`
        ? Param | ExtractParams<`/${Rest}`>
        : //   head   :   param  (last segment)
          S extends `${infer _Start}:${infer Param}`
            ? Param
            : // no more colon‑segments
              never;
```

`ExtractParams<'/users/:userId/posts/:postId'>` → `"userId" | "postId"`.

### 1.2  Enforce *exact* correspondence

We need two things:

* every key that appears in the template **must** exist in the object,
* **no extra keys** are allowed.

```ts
// Helper that makes a type “exactly the keys K”.
type Exact<T, K extends keyof any> =
    // T must contain at least the required keys …
    T extends Record<K, string>
        // … and it must not contain any other keys.
        ? Exclude<keyof T, K> extends never
            ? T
            : never
        : never;
```

### 1.3  The `createRoute` signature

```ts
function createRoute<
    Path extends string,
    // the user‑provided object is first captured as `P`
    P extends Record<string, string>,
    // … then we verify that it is an Exact match for the extracted keys.
    Params extends Exact<P, ExtractParams<Path>>
>(path: Path, params: Params): { path: Path; params: Params } {
    // the implementation is irrelevant for the type‑check
    return { path, params };
}
```

### 1.4  Example usage

```ts
// ✅ correct – keys match the template
createRoute('/users/:userId/posts/:postId', {
    userId: '123',
    postId: '456',
});

// ❌ missing key – compile‑tim...
```

### Gemini 3 Flash Preview

**Generation Time:** 8750ms
**Tokens:** 1033

```
Here are the TypeScript implementations for both constraints using template literal types and recursive mapping.

### 1. Type-Safe Route Parameters
This uses **Template Literal Types** to recursively parse the string and extract segments starting with a colon.

```typescript
type ExtractRouteParams<T extends string> =
  T extends `${infer _Start}:${infer Param}/${infer Rest}`
    ? { [K in Param | keyof ExtractRouteParams<Rest>]: string }
    : T extends `${infer _Start}:${infer Param}`
    ? { [K in Param]: string }
    : {};

function createRoute<Path extends string>(
  path: Path,
  params: ExtractRouteParams<Path>
) {
  return { path, params };
}

// --- Examples ---
// ✓ Success
createRoute('/users/:userId/posts/:postId', { 
  userId: '123', 
  postId: '456' 
});

// ✗ Error: Property 'wrongParam' does not exist...
// @ts-expect-error
createRoute('/users/:userId', { wrongParam: '123' });

// ✗ Error: Property 'postId' is missing...
// @ts-expect-error
createRoute('/users/:userId/posts/:postId', { userId: '123' });
```

---

### 2. Sequential Builder Pattern
This uses **Interface Chaining**. By returning a different interface at every step, we enforce both the specific order and the requirement that all methods must be called before `build()` is available.

```typescript
interface IBuild {
  build(): { name: string; age: number };
}

interface ISetAge {
  setAge(age: number): IBuild;
}

interface ISetName {
  setName(name: string): ISetAge;
}

class Builder implements ISetName, ISetAge, IBuild {
  private name!: string;
  private age!: number;

  static init(): ISetName {
    return new Builder();
  }

  setName(name: string): ISetAge {
    this.name = name;
    return this;
  }

  setAge(age: number): IBuild {
    this.age = age;
    return this;
  }

  build() {
    return { name: this.name, age: this.age };
  }
}

// --- Examples ---
const builder = Builder.init();

// ✓ Success: Correct order and completeness
builder.setName('Alice').setAge(25).build();

// ...
```

### MiniMax M2.5

**Generation Time:** 31546ms
**Tokens:** 2267

```

```

### MiMo-V2-Flash

**Generation Time:** 14566ms
**Tokens:** 1777

```
Here are the TypeScript type definitions that enforce these compile-time constraints using Template Literal Types, Variadic Tuple Types, and Recursive Types.

### 1. Route Type with Path Parameter Matching

This type extracts the placeholders from the path string (e.g., `:userId`) and enforces that the provided params object contains exactly those keys.

```typescript
// 1. Extract parameter names from a string literal type
// E.g., ExtractParams<'/users/:userId/posts/:postId'> -> 'userId' | 'postId'
type ExtractParams<T extends string> = 
  T extends `${string}:${infer Param}/${infer Rest}`
    ? Param | ExtractParams<Rest>
    : T extends `${string}:${infer Param}`
    ? Param
    : never;

// 2. Define the Route type
// It takes a path string and enforces that the params object has keys matching the path placeholders
type Route<Path extends string, Params extends Record<ExtractParams<Path>, string>> = {
  path: Path;
  params: Params;
};

// 3. The createRoute function
// We use a generic constraint to ensure the second argument matches the keys extracted from the first
declare function createRoute<
  Path extends string, 
  ParamsKeys extends ExtractParams<Path>
>(
  path: Path, 
  params: Record<ParamsKeys, string>
): Route<Path, Record<ParamsKeys, string>>;

// --- Usage Examples ---

// ✓ Valid: userId and postId match the path
const validRoute = createRoute('/users/:userId/posts/:postId', { 
  userId: '123', 
  postId: '456' 
});

// ✗ Compile Error: Object may specify 'userId', but is missing required 'postId'
// const invalidRoute = createRoute('/users/:userId/posts/:postId', { 
//   userId: '123' 
// });

// ✗ Compile Error: 'wrongParam' does not exist in type 'Record<"userId", string>'
// const wrongParamRoute = createRoute('/users/:userId', { 
//   wrongParam: '123' 
// });

// ✗ Compile Error: 'extraParam' does not exist in type 'Record<"userId", string>'
// const extraParamRoute = createRoute('/users/:userId', { 
//   userId: '123', 
//   extraParam: ...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*