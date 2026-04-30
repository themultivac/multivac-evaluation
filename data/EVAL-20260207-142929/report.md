# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260207-142929
**Timestamp:** 2026-02-07T14:29:29.220728
**Category:** Programming & Code
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
| 1 | Claude Sonnet 4.5 | 9.49 | 8.80 | 10.00 | 0.42 |
| 2 | Grok 3 (Direct) | 9.42 | 8.80 | 9.80 | 0.39 |
| 3 | GPT-5.2-Codex | 9.36 | 8.60 | 9.80 | 0.54 |
| 4 | Gemini 3 Flash Preview | 9.28 | 8.60 | 9.80 | 0.48 |
| 5 | Grok Code Fast 1 | 9.16 | 8.25 | 10.00 | 0.65 |
| 6 | Claude Opus 4.5 | 9.07 | 7.80 | 9.80 | 0.67 |
| 7 | DeepSeek V3.2 | 8.84 | 6.80 | 10.00 | 1.10 |
| 8 | Gemini 3 Pro Preview | 5.62 | 4.10 | 7.20 | 1.06 |
| 9 | GLM 4.7 | 4.25 | 0.50 | 8.55 | 4.15 |
| 10 | MiniMax M2.1 | 4.24 | 0.50 | 8.15 | 3.92 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | Claude Opus 4.5 | 6.46 |
| 2 | Claude Sonnet 4.5 | 6.65 |
| 3 | GPT-5.2-Codex | 7.95 |
| 4 | Grok 3 (Direct) | 8.39 |
| 5 | DeepSeek V3.2 | 8.73 |
| 6 | MiniMax M2.1 | 8.99 |
| 7 | Grok Code Fast 1 | 9.09 |
| 8 | GLM 4.7 | 9.14 |
| 9 | Gemini 3 Flash Preview | 9.32 |

**Strictest Judge:** claude_opus
**Most Lenient Judge:** gemini_3_flash
**Total Judgments:** 100
**Valid Judgments:** 72

---

## Model Pool

Models selected for **Programming & Code** evaluation:

1. **Grok Code Fast 1** (openrouter)
2. **Claude Opus 4.5** (openrouter)
3. **Gemini 3 Flash Preview** (openrouter)
4. **Claude Sonnet 4.5** (openrouter)
5. **Gemini 3 Pro Preview** (openrouter)
6. **MiniMax M2.1** (openrouter)
7. **GLM 4.7** (openrouter)
8. **DeepSeek V3.2** (openrouter)
9. **GPT-5.2-Codex** (openrouter)
10. **Grok 3 (Direct)** (xai)

---

## Model Responses

### Grok Code Fast 1

**Generation Time:** 12884ms
**Tokens:** 2796

```
### TypeScript Types for Route and Builder Patterns

Below, I'll provide the TypeScript type definitions and example usage for both constraints. These use advanced TypeScript features like template literal types, conditional types, and generics to enforce compile-time constraints.

#### 1. Route Type with Path Parameter Matching

The `Route` type ensures that the provided `params` object exactly matches the path parameters extracted from the URL template string. Path parameters are identified by the `:paramName` syntax (e.g., `:userId`). The `createRoute` function is generic over the template string, and its `params` argument is typed to require exactly the matching keys (no more, no less).

```typescript
// Utility type to extract parameter names from a route template
type ExtractRouteParams<T> = T extends `${string}:${infer P}/${infer R}`
  ? P | ExtractRouteParams<R>
  : T extends `${string}:${infer P}`
  ? P
  : never;

// Type for the params object, enforcing exact match
type RouteParams<T> = Record<ExtractRouteParams<T>, string>;

// Example Route type (could be extended for more properties)
type Route<T extends string> = {
  template: T;
  params: RouteParams<T>;
};

// Function to create a route
function createRoute<T extends string>(template: T, params: RouteParams<T>): Route<T> {
  return { template, params };
}

// Example usage
const validRoute = createRoute('/users/:userId/posts/:postId', { userId: '123', postId: '456' }); // ✓ Compiles
// const invalidRoute1 = createRoute('/users/:userId', { wrongParam: '123' }); // ✗ Compile error: 'wrongParam' does not exist in type '{}'
// const invalidRoute2 = createRoute('/users/:userId/posts/:postId', { userId: '123' }); // ✗ Compile error: Property 'postId' is missing
// const invalidRoute3 = createRoute('/users/:userId/posts/:postId', { userId: '123', postId: '456', extra: '789' }); // ✗ Compile error: 'extra' does not exist in type '{}'
```

- **How it works**: `ExtractRouteParams` recursively parses the templ...
```

### Claude Opus 4.5

**Generation Time:** 28438ms
**Tokens:** 2254

```
# Advanced TypeScript Compile-Time Constraints

## 1. Type-Safe Route Parameters

This implementation extracts path parameters from URL templates and enforces matching params objects.

```typescript
// ============================================================
// ROUTE TYPE WITH PATH PARAMETER EXTRACTION
// ============================================================

/**
 * Extracts parameter names from a URL path template
 * '/users/:userId/posts/:postId' → 'userId' | 'postId'
 */
type ExtractRouteParams<Path extends string> =
  Path extends `${infer _Start}:${infer Param}/${infer Rest}`
    ? Param | ExtractRouteParams<`/${Rest}`>
    : Path extends `${infer _Start}:${infer Param}`
      ? Param
      : never;

/**
 * Creates a params object type from extracted parameter names
 * 'userId' | 'postId' → { userId: string; postId: string }
 */
type RouteParams<Path extends string> = {
  [K in ExtractRouteParams<Path>]: string;
};

/**
 * Route type that links a path template to its required params
 */
interface Route<Path extends string> {
  path: Path;
  params: RouteParams<Path>;
  // Computed full URL
  url: string;
}

/**
 * Creates a type-safe route
 * Compile-time error if params don't match the path template
 */
function createRoute<Path extends string>(
  path: Path,
  params: RouteParams<Path>
): Route<Path> {
  // Build the actual URL by replacing parameters
  let url: string = path;
  
  for (const [key, value] of Object.entries(params as Record<string, string>)) {
    url = url.replace(`:${key}`, value);
  }
  
  return {
    path,
    params,
    url,
  };
}

// ============================================================
// USAGE EXAMPLES
// ============================================================

// ✅ Correct usage - all params provided
const userPostRoute = createRoute(
  '/users/:userId/posts/:postId',
  { userId: '123', postId: '456' }
);
console.log(userPostRoute.url); // '/users/123/posts/456'

// ✅ Correct usage - single param
const userRo...
```

### Gemini 3 Flash Preview

**Generation Time:** 6171ms
**Tokens:** 1030

```
Here are the TypeScript implementations for both constraints using template literal types and interface chaining.

### 1. Route Path Parameter Enforcement

This uses recursive template literal types to parse the string and extract keys starting with `:`.

```typescript
type ExtractRouteParams<T extends string> =
  T extends `${infer _Start}:${infer Param}/${infer Rest}`
    ? Param | ExtractRouteParams<Rest>
    : T extends `${infer _Start}:${infer Param}`
    ? Param
    : never;

// This maps the extracted keys into a required object type
type RouteParams<Path extends string> = {
  [K in ExtractRouteParams<Path>]: string;
};

// If no params are found, the second argument should be an empty object or omitted
function createRoute<Path extends string>(
  path: Path,
  params: RouteParams<Path>
) {
  let url: string = path;
  for (const [key, value] of Object.entries(params)) {
    url = url.replace(`:${key}`, value as string);
  }
  return url;
}

/** USAGE **/
// ✓ Success
createRoute('/users/:userId/posts/:postId', { userId: '123', postId: '456' });

// ✗ Error: Property 'wrongParam' does not exist
createRoute('/users/:userId', { wrongParam: '123' }); 

// ✗ Error: Property 'postId' is missing
createRoute('/users/:userId/posts/:postId', { userId: '123' }); 
```

---

### 2. Ordered Builder Pattern

To enforce order and completeness, we return different interfaces at each step. This creates a "Finite State Machine" at the type level.

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

  static start(): ISetName {
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
    return { name: thi...
```

### Claude Sonnet 4.5

**Generation Time:** 23779ms
**Tokens:** 1837

```
# TypeScript Compile-Time Constraints

## 1. Route Type with Path Parameter Validation

```typescript
// Extract path parameters from a route string
type ExtractRouteParams<T extends string> = 
  T extends `${infer _Start}:${infer Param}/${infer Rest}`
    ? Param | ExtractRouteParams<Rest>
    : T extends `${infer _Start}:${infer Param}`
    ? Param
    : never;

// Create a record type from extracted parameters
type RouteParams<T extends string> = 
  ExtractRouteParams<T> extends never
    ? Record<string, never>  // No params required
    : Record<ExtractRouteParams<T>, string>;

// Route creation function
function createRoute<T extends string>(
  path: T,
  params: RouteParams<T>
): string {
  let result = path as string;
  
  for (const [key, value] of Object.entries(params)) {
    result = result.replace(`:${key}`, value);
  }
  
  return result;
}

// ✓ Valid examples
const route1 = createRoute('/users/:userId/posts/:postId', {
  userId: '123',
  postId: '456'
});

const route2 = createRoute('/users/:userId', {
  userId: '123'
});

const route3 = createRoute('/static/path', {});

// ✗ Compile errors
// @ts-expect-error - Wrong parameter name
const route4 = createRoute('/users/:userId', {
  wrongParam: '123'
});

// @ts-expect-error - Missing required parameter
const route5 = createRoute('/users/:userId/posts/:postId', {
  userId: '123'
});

// @ts-expect-error - Extra parameter
const route6 = createRoute('/users/:userId', {
  userId: '123',
  extraParam: '456'
});

console.log(route1); // "/users/123/posts/456"
```

## 2. Builder Pattern with Ordered Method Calls

```typescript
// State tracking types
type BuilderState = {
  name: boolean;
  age: boolean;
};

// The built result
type Person = {
  name: string;
  age: number;
};

// Builder class with state tracking
class PersonBuilder<State extends BuilderState = { name: false; age: false }> {
  private data: Partial<Person> = {};

  // setName can only be called when name is false (not yet set)
  setName<S e...
```

### Gemini 3 Pro Preview

**Generation Time:** 20730ms
**Tokens:** 2233

```
Here are the TypeScript type definitions to enforce these constraints.

### 1. Strongly Typed Route Parameters
We use **Template Literal Types** and recursive conditional types to parse the URL string and extract substrings starting with `:`.

```typescript
// --- Type Definitions ---

// 1. Recursive type to extract params starting with ':'
type ExtractParams<Path extends string> = 
  Path extends `${infer Start}:${infer Param}/${infer Rest}` 
    ? Param | ExtractParams<`/${Rest}`> // Recurse if there is more path after '/'
    : Path extends `${infer Start}:${infer Param}` 
      ? Param // End of string case
      : never;

// 2. The function definition utilizing the extracted keys
function createRoute<P extends string>(
  path: P, 
  // We map over the extracted union type to create the required object shape
  params: { [K in ExtractParams<P>]: string }
): string {
  let result = path as string;
  for (const key in params) {
    result = result.replace(`:${key}`, (params as any)[key]);
  }
  return result;
}

// --- Usage Examples ---

// ✅ Valid: Params match exactly
createRoute('/users/:userId/posts/:postId', { 
  userId: '123', 
  postId: '456' 
});

// ✅ Valid: Single param
createRoute('/profile/:username', { 
  username: 'jdoe' 
});

// ❌ Error: Missing 'postId'
// @ts-expect-error
createRoute
```

### MiniMax M2.1

**Generation Time:** 24876ms
**Tokens:** 2269

```

```

### GLM 4.7

**Generation Time:** 29858ms
**Tokens:** 2223

```

```

### DeepSeek V3.2

**Generation Time:** 45724ms
**Tokens:** 1364

```
Here are TypeScript types that enforce these compile-time constraints:

## 1. Route Type with Path Parameter Validation

```typescript
// Extract parameters from a URL template
type ExtractParams<T extends string> =
  T extends `${infer Start}:${infer Param}/${infer Rest}`
    ? { [K in Param | keyof ExtractParams<Rest>]: string }
    : T extends `${infer Start}:${infer Param}`
    ? { [K in Param]: string }
    : {};

// Type-safe route creator
function createRoute<
  TPath extends string,
  TParams extends ExtractParams<TPath>
>(
  path: TPath,
  params: TParams extends Record<string, string> ? TParams : never
): { path: TPath; params: TParams } {
  return { path, params };
}

// Example usage
const validRoute = createRoute('/users/:userId/posts/:postId', {
  userId: '123',
  postId: '456'
}); // ✓ Compiles

// These will cause compile errors:
// const invalidRoute1 = createRoute('/users/:userId', { wrongParam: '123' }); // ✗
// const invalidRoute2 = createRoute('/users/:userId', {}); // ✗
// const invalidRoute3 = createRoute('/users/:userId', { userId: 123 }); // ✗
```

## 2. Builder Pattern with Method Order Enforcement

```typescript
// Builder state machine types
type EmptyBuilder = { _state: 'empty' };
type WithName = { _state: 'nameSet'; name: string };
type WithAge = { _state: 'ageSet'; age: number };
type WithBoth = { _state: 'bothSet'; name: string; age: number };

class Builder<T extends { _state: string }> {
  private state: T;

  constructor(state: T) {
    this.state = state;
  }

  // setName can only be called on empty builder
  setName<K extends T extends EmptyBuilder ? string : never>(
    name: K
  ): Builder<WithName> {
    return new Builder<WithName>({ _state: 'nameSet', name });
  }

  // setAge can only be called after setName
  setAge<K extends T extends WithName ? number : never>(
    age: K
  ): Builder<WithBoth> {
    const withName = this.state as WithName;
    return new Builder<WithBoth>({
      _state: 'bothSet',
      name: withName...
```

### GPT-5.2-Codex

**Generation Time:** 18595ms
**Tokens:** 1364

```
Below is a clean, type‑safe solution using **template‑literal types** and **stateful builder interfaces**.

---

## ✅ 1) Route type — URL params must match params object

```ts
// Extract `:param` names from a URL template
type ExtractRouteParams<Path extends string> =
  Path extends `${string}:${infer Param}/${infer Rest}`
    ? Param | ExtractRouteParams<`/${Rest}`>
    : Path extends `${string}:${infer Param}`
      ? Param
      : never;

// Build params object from extracted names
type RouteParams<Path extends string> = {
  [K in ExtractRouteParams<Path>]: string;
};

type Route<Path extends string> = {
  path: Path;
  params: RouteParams<Path>;
};

declare function createRoute<P extends string>(
  path: P,
  params: RouteParams<P>
): Route<P>;
```

### ✅ Usage

```ts
createRoute('/users/:userId/posts/:postId', {
  userId: '123',
  postId: '456',
}); // OK

createRoute('/users/:userId', {
  wrongParam: '123',
}); // ❌ compile error
```

---

## ✅ 2) Builder pattern — enforce call order

```ts
type BuilderStart = {
  setName(name: string): BuilderWithName;
};

type BuilderWithName = {
  setAge(age: number): BuilderComplete;
};

type BuilderComplete = {
  build(): { name: string; age: number };
};

declare const builder: BuilderStart;
```

### ✅ Usage

```ts
builder.setName('x').setAge(25).build(); // ✅ OK

builder.setAge(25).setName('x').build(); // ❌ error (setAge not allowed)

builder.setName('x').build(); // ❌ error (age not set)
```

---

These type definitions enforce the constraints **at compile time** using TypeScript’s type system alone.
```

### Grok 3 (Direct)

**Generation Time:** 13917ms
**Tokens:** 1471

```
Let's create TypeScript types for both scenarios with detailed explanations.

### 1. Route Type with Path Parameter Matching

We'll use TypeScript's template literal types and mapped types to extract path parameters and ensure they match the provided params object.

```typescript
// Utility type to extract parameters from a path template
type ExtractParams<Path extends string> =
  Path extends `${infer _Start}:${infer Param}/${infer Rest}`
    ? { [K in Param]: string } & ExtractParams<`/${Rest}`>
    : Path extends `${infer _Start}:${infer Param}`
    ? { [K in Param]: string }
    : {};

// Route creation function with type constraints
function createRoute<Path extends string>(
  path: Path,
  params: ExtractParams<Path>
): { path: string; params: Record<string, string> } {
  return { path, params };
}

// Example usage
// Valid case
const validRoute = createRoute('/users/:userId/posts/:postId', {
  userId: '123',
  postId: '456',
});

// Invalid cases - these will cause compile-time errors
// Missing parameters
// @ts-expect-error
const missingParam = createRoute('/users/:userId', {});

// Wrong parameter name
// @ts-expect-error
const wrongParam = createRoute('/users/:userId', { wrongId: '123' });

// Extra parameter
// @ts-expect-error
const extraParam = createRoute('/users/:userId', { userId: '123', extra: '456' });
```

**Explanation:**
- `ExtractParams<Path>` is a recursive type that parses the path string and creates an object type with keys matching the parameter names (e.g., `:userId` becomes `userId: string`).
- The `createRoute` function uses this type to enforce that the `params` argument matches the extracted parameters from the path.
- TypeScript will throw compile-time errors if the params object doesn't exactly match the expected structure (missing, extra, or wrong parameter names).

### 2. Builder Pattern with Method Order Enforcement

We'll use a state machine approach with interfaces to enforce method call order. Each method returns a new type t...
```

---

*Generated by The Multivac V5*
*https://multivac.com*