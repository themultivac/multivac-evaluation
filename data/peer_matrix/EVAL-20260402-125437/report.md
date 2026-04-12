# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-125437
**Timestamp:** 2026-04-02T12:54:37.341722
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
| 1 | Claude Sonnet 4.6 | 9.14 | 8.40 | 10.00 | 0.48 |
| 2 | Claude Opus 4.6 | 9.04 | 8.20 | 10.00 | 0.59 |
| 3 | GPT-5.4 | 8.94 | 8.40 | 9.80 | 0.52 |
| 4 | Gemini 3 Flash Preview | 8.72 | 8.30 | 9.45 | 0.36 |
| 5 | MiMo-V2-Flash | 8.49 | 7.35 | 9.80 | 0.87 |
| 6 | DeepSeek V3 | 7.71 | 6.55 | 9.80 | 1.06 |
| 7 | Grok 4.20 | 7.64 | 5.75 | 9.55 | 1.35 |
| 8 | GPT-OSS-120B | 6.91 | 3.25 | 9.05 | 2.07 |
| None | Gemini 3.1 Pro | 2.13 | 0.45 | 5.05 | 1.65 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 6.14 |
| 2 | Claude Sonnet 4.6 | 7.29 |
| 3 | GPT-OSS-120B | 7.40 |
| 4 | Claude Opus 4.6 | 7.61 |
| 5 | MiMo-V2-Flash | 8.03 |
| 6 | Gemini 3.1 Pro | 8.04 |
| 7 | MiniMax M2.5 | 8.04 |
| 8 | Grok 4.20 | 8.42 |
| 9 | Gemini 3 Flash Preview | 8.65 |
| 10 | DeepSeek V3 | 8.73 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** deepseek_v4
**Total Judgments:** 100
**Valid Judgments:** 75

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

**Generation Time:** 10534ms
**Tokens:** 791

```
```ts
// =========================
// 1. Route path params match
// =========================

// Extract `:param` names from a route string
type ExtractRouteParams<Path extends string> =
  Path extends `${string}:${infer Param}/${infer Rest}`
    ? Param | ExtractRouteParams<`/${Rest}`>
    : Path extends `${string}:${infer Param}`
      ? Param
      : never;

// Params object must contain exactly the extracted keys
type RouteParams<Path extends string> = {
  [K in ExtractRouteParams<Path>]: string;
};

// Helper to reject extra keys
type Exact<Expected, Actual extends Expected> =
  Expected & {
    [K in Exclude<keyof Actual, keyof Expected>]: never;
  };

// Route type
type Route<Path extends string> = {
  path: Path;
  params: RouteParams<Path>;
};

// Factory
function createRoute<
  Path extends string,
  Params extends RouteParams<Path>
>(
  path: Path,
  params: Exact<RouteParams<Path>, Params>
): Route<Path> {
  return { path, params };
}

// ===== Usage =====

const okRoute = createRoute(
  '/users/:userId/posts/:postId',
  { userId: '123', postId: '456' }
); // ✓

const badRoute1 = createRoute(
  '/users/:userId',
  { wrongParam: '123' }
  //            ~~~~~~~~~ compile error
);

const badRoute2 = createRoute(
  '/users/:userId',
  {}
  // compile error: missing userId
);

const badRoute3 = createRoute(
  '/users/:userId',
  { userId: '123', extra: 'nope' }
  //                 ~~~~~ compile error
);


// =========================
// 2. Ordered Builder pattern
// =========================

type Person = {
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
  build(): Person;
};

// Concrete builder value typed by stages
const builder: NameStage = {
  setName(name: string): AgeStage {
    return {
      setAge(age: number): BuildStage {
        return {
          build(): Person {
            return { name, age };
          }
        };
  ...
```

### Claude Opus 4.6

**Generation Time:** 33292ms
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
 * Builds the required params object type from a URL template.
 * "/users/:userId" → { userId: string }
 */
type RouteParams<T extends string> = {
  [K in ExtractRouteParams<T>]: string;
};

/**
 * The Route type couples a path template with its extracted params.
 */
interface Route<T extends string> {
  path: T;
  params: RouteParams<T>;
  // Computed full URL after parameter substitution
  toURL(): string;
}

/**
 * Creates a type-safe route. The params object MUST contain exactly
 * the parameters declared in the URL template — no more, no less.
 */
function createRoute<T extends string>(
  path: T,
  // Enforce EXACT match: params must have all route keys, and
  // no extra keys are allowed via the two-way constraint.
  ...args: ExtractRouteParams<T> extends never
    ? []  // No params needed for paths like "/health"
    : [params: RouteParams<T> & Record<string, string>]
): Route<T> {
  const params = (args[0] ?? {}) as RouteParams<T>;

  return {
    path,
    params,
    toURL(): string {
      let url: string = path;
      for (const [key, value] of Object.entries(params)) {
        url = url.replace(`:${key}`, value);
      }
      return url;
    },
  };
}

// ---------- Compile-time verification tests ----------

// ✅ VALID: params exactly match the template
const userPostRoute = createRoute(
  '/users/:userId/p...
```

### Gemini 3.1 Pro

**Generation Time:** 24623ms
**Tokens:** 2233

```
build()` ✓
        *   `builder.setAge(25)` ✗ (`setAge` doesn't exist on `BuilderState1`)
        *   `builder.setName('x').build()` ✗ (`build` doesn't exist on `BuilderState2`)
    *   *Refining for realism:* Let's provide a real implementation
```

### Claude Sonnet 4.6

**Generation Time:** 30465ms
**Tokens:** 2254

```
# TypeScript Compile-Time Constraint Types

## Part 1: Route Path Parameter Extraction

```typescript
// ============================================================
// UTILITY TYPES: Extract path parameters from URL templates
// ============================================================

/**
 * Extracts parameter names from a path template string.
 * '/users/:userId/posts/:postId' → 'userId' | 'postId'
 */
type ExtractPathParams<Path extends string> =
  Path extends `${infer _Before}:${infer Param}/${infer Rest}`
    ? Param | ExtractPathParams<`/${Rest}`>
    : Path extends `${infer _Before}:${infer Param}`
    ? Param
    : never;

/**
 * Builds a params object type from extracted parameter names.
 * 'userId' | 'postId' → { userId: string; postId: string }
 */
type ParamsFromPath<Path extends string> = {
  [K in ExtractPathParams<Path>]: string;
};

/**
 * Validates that the provided params exactly match the path params.
 * Ensures no extra keys and no missing keys.
 */
type ValidateParams<
  Path extends string,
  Params extends Record<string, string>
> = ExtractPathParams<Path> extends never
  ? // Path has no params — params object must be empty
    Params extends Record<string, never>
      ? Params
      : "Error: Path has no parameters but params were provided"
  : // Params must exactly match extracted keys (no extra, no missing)
    keyof Params extends ExtractPathParams<Path>
    ? ExtractPathParams<Path> extends keyof Params
      ? Params
      : `Error: Missing required params: ${Exclude<
          ExtractPathParams<Path> & string,
          keyof Params & string
        >}`
    : `Error: Unknown params provided: ${Exclude<
        keyof Params & string,
        ExtractPathParams<Path> & string
      >}`;

// ============================================================
// ROUTE TYPE & FACTORY
// ============================================================

interface Route<Path extends string> {
  path: Path;
  params: ParamsFromPath<Path>;
  /** Res...
```

### Grok 4.20

**Generation Time:** 7243ms
**Tokens:** 1253

```
**Solution: TypeScript Types with Compile-Time Enforcement**

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
  return path.replace(/:(\w+)/g, (_, key) => String(params[key]));
};

// Example usage:
createRoute('/users/:userId/posts/:postId', { 
  userId: '123', 
  postId: '456' 
}); // ✓ OK

createRoute('/users/:userId', { 
  userId: '123' 
}); // ✓ OK

// These will cause compile errors:
createRoute('/users/:userId', { 
  wrongParam: '123' // ✗ Missing 'userId'
});

createRoute('/users/:userId', { 
  userId: '123',
  extraParam: 'x' // ✗ Extra property
});
```

---

### 2. Builder Pattern with Strict Call Order

```ts
type BuilderState = 'empty' | 'name' | 'complete';

class Builder<T extends BuilderState = 'empty'> {
  private name?: string;
  private age?: number;

  setName(name: string): Builder<'name'> {
    this.name = name;
    return this as any;
  }

  setAge(age: number): Builder<'complete'> {
    if ('name' in (this as any)) {
      this.age = age;
      return this as any;
    }
    throw new Error('Name must be set before age');
  }

  build(): { name: string; age: number } {
    if (!this.name || this.age === undefined) {
      throw new Error('Both name and age must be set');
    }
    return { name: this.name, age: this.age };
  }
}

// Factory function to start the chain
function createBuilder(): Builder<'empty'> {
  return new Builder<'empty'>();
}

// Example usage:
const result = createBuilder()
  .setName('Alice')
  .setAge(30)
  .build(); 
// ✓ OK - returns { name: string; age: number }

// These will cause compile-t...
```

### DeepSeek V3

**Generation Time:** 24597ms
**Tokens:** 1070

```
Here are TypeScript types that enforce those compile-time constraints:

### 1. Route Type with Path Parameter Validation

```typescript
type ExtractPathParams<T extends string> =
    T extends `${infer _}:${infer Param}/${infer Rest}`
    ? Param | ExtractPathParams<Rest>
    : T extends `${infer _}:${infer Param}`
    ? Param
    : never;

type ValidateParams<Path extends string, Params extends Record<string, any>> = 
    Record<ExtractPathParams<Path>, string> extends Params
    ? Params
    : { error: `Missing or invalid params. Expected: ${ExtractPathParams<Path>}` };

function createRoute<Path extends string>(
    path: Path,
    params: ValidateParams<Path, Record<string, any>>
): { path: Path, params: typeof params } {
    return { path, params };
}

// Example usage:
const validRoute = createRoute('/users/:userId/posts/:postId', { 
    userId: '123', 
    postId: '456' 
}); // ✓

const invalidRoute = createRoute('/users/:userId', { 
    wrongParam: '123' 
}); // ✗ Compile error: Type '{ wrongParam: string; }' is not assignable to type '{ error: "Missing or invalid params. Expected: userId"; }'
```

### 2. Builder Pattern with Ordered Method Chaining

```typescript
type NoNameBuilder = {
    setName: <Name extends string>(name: Name) => HasNameBuilder<Name>;
    setAge: never; // Can't call setAge before setName
    build: never;  // Can't call build yet
};

type HasNameBuilder<Name extends string> = {
    setName: never; // Can't call setName again
    setAge: <Age extends number>(age: Age) => HasNameAndAgeBuilder<Name, Age>;
    build: never;   // Can't call build yet
};

type HasNameAndAgeBuilder<Name extends string, Age extends number> = {
    setName: never; // Can't call setName again
    setAge: never;  // Can't call setAge again
    build: () => { name: Name, age: Age };
};

const builder: NoNameBuilder = {
    setName(name) {
        return {
            setName: () => { throw new Error("Can't set name twice") },
            setAge(age) {
           ...
```

### GPT-OSS-120B

**Generation Time:** 52558ms
**Tokens:** 2280

```
Below are two **stand‑alone** type‑level solutions that you can copy‑paste into a TypeScript file (TS 4.5+).  
Both solutions compile to JavaScript that works exactly like the examples, but the *type system* will reject the illegal calls already at compile time.

---

## 1️⃣  `createRoute` – URL‑template ↔ params object

```ts
/* ----------------------------------------------------------------------
   1️⃣  Extract the names of the “:param” parts from a literal string.
   ---------------------------------------------------------------------- */
type ExtractParams<T extends string> =
    //  “…/:p/…”  →  take the part after the colon, then recurse
    T extends `${infer _Before}:${infer Param}/${infer Rest}`
        ? Param | ExtractParams<`/${Rest}`>
        : //  “…/:p”  (no more slash) → take the final part
          T extends `${infer _Before}:${infer Param}`
            ? Param
            : never;

/* ----------------------------------------------------------------------
   2️⃣  Helper that makes an *exact* object type – no missing keys,
       no extra keys.
   ---------------------------------------------------------------------- */
type Exact<P, Shape> =
    //   P must be assignable to Shape …
    P extends Shape
        // … and must not contain keys that Shape does not have
        ? Exclude<keyof P, keyof Shape> extends never
            ? P
            : never
        : never;

/* ----------------------------------------------------------------------
   3️⃣  The public API
   ---------------------------------------------------------------------- */
declare function createRoute<
    T extends string,
    // every extracted param must exist in the object and be a string
    P extends Record<ExtractParams<T>, string>
>(
    path: T,
    // `Exact` guarantees that *only* those keys are present
    params: Exact<P, Record<ExtractParams<T>, string>>
): { path: T; params: P };

/* ----------------------------------------------------------------------
   4️⃣  E...
```

### Gemini 3 Flash Preview

**Generation Time:** 7938ms
**Tokens:** 1035

```
Here are the TypeScript implementations for both constraints using advanced template literal types and recursive mapping.

### 1. Route Parameter Enforcement
We use a recursive type to parse the string literal and extract segments starting with `:`.

```typescript
type ExtractRouteParams<T extends string> =
  T extends `${infer _Start}:${infer Param}/${infer Rest}`
    ? Param | ExtractRouteParams<`/${Rest}`>
    : T extends `${infer _Start}:${infer Param}`
    ? Param
    : never;

// This type ensures the object keys exactly match the extracted params
type RouteParams<Path extends string> = 
  [ExtractRouteParams<Path>] extends [never] 
    ? Record<string, never> 
    : { [K in ExtractRouteParams<Path>]: string };

function createRoute<T extends string>(path: T, params: RouteParams<T>) {
  return { path, params };
}

// --- Usage ---
// ✓ Success
createRoute('/users/:userId/posts/:postId', { userId: '123', postId: '456' });

// ✗ Error: Property 'postId' is missing
// @ts-expect-error
createRoute('/users/:userId/posts/:postId', { userId: '123' });

// ✗ Error: 'wrongParam' does not exist in type
// @ts-expect-error
createRoute('/users/:userId', { wrongParam: '123' });
```

---

### 2. Sequential Builder Pattern
We enforce order by returning different interfaces at each step. By using specific return types, we "unlock" the next method in the sequence and hide the previous ones.

```typescript
interface IBuilderFinal {
  build(): { name: string; age: number };
}

interface IBuilderAge {
  setAge(age: number): IBuilderFinal;
}

interface IBuilderName {
  setName(name: string): IBuilderAge;
}

class SequentialBuilder implements IBuilderName, IBuilderAge, IBuilderFinal {
  private name!: string;
  private age!: number;

  setName(name: string): IBuilderAge {
    this.name = name;
    return this;
  }

  setAge(age: number): IBuilderFinal {
    this.age = age;
    return this;
  }

  build() {
    return { name: this.name, age: this.age };
  }
}

const builder: IBuilde...
```

### MiniMax M2.5

**Generation Time:** 51784ms
**Tokens:** 2264

```

```

### MiMo-V2-Flash

**Generation Time:** 9679ms
**Tokens:** 1172

```
```typescript
// ============================================================
// 1. Route Type: URL Template Params vs Params Object
// ============================================================

/**
 * Extracts parameter names from a URL template string.
 * E.g., ExtractRouteParams<"/users/:userId/posts/:postId"> => "userId" | "postId"
 */
type ExtractRouteParams<T extends string> =
  T extends `${string}:${infer Param}/${infer Rest}`
    ? Param | ExtractRouteParams<Rest>
    : T extends `${string}:${infer Param}`
      ? Param
      : never;

/**
 * Creates a strongly-typed route builder.
 *
 * @param template - The URL path containing :param placeholders
 * @param params - An object where keys must match the extracted param names
 */
export function createRoute<
  T extends string,
  P extends Record<ExtractRouteParams<T>, string>
>(template: T, params: P): string {
  let url = template;
  (Object.keys(params) as (keyof P)[]).forEach((key) => {
    url = url.replace(`:${String(key)}`, params[key as keyof P]);
  });
  return url;
}

// --- Examples for Route ---

// ✅ Valid: All params present
const route1 = createRoute('/users/:userId/posts/:postId', {
  userId: '123',
  postId: '456',
});

// ❌ Compile Error: 'wrongParam' does not exist in type '{ userId: string; postId: string; }'
// const route2 = createRoute('/users/:userId/posts/:postId', {
//   wrongParam: '123'
// });

// ❌ Compile Error: 'userId' is missing
// const route3 = createRoute('/users/:userId/posts/:postId', {
//   postId: '456'
// });

// ✅ Valid: No params in template, empty object allowed
const route4 = createRoute('/home', {});


// ============================================================
// 2. Builder Pattern: Enforced Method Order
// ============================================================

// --- State Tokens (Brands) ---
// These represent the "state" of the builder. 
// We use unique symbols or string literals to make them distinct.
type Step1_NameSet = { readonly _step: 'nam...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*