# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-151829
**Timestamp:** 2026-04-02T15:18:29.690079
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

Design a GraphQL schema for a social media platform with users, posts, comments, likes, and follows. Address: N+1 query problem with DataLoader pattern, cursor-based pagination, proper input validation, rate limiting per field, and subscription for real-time updates. Include resolver implementations for the trickiest queries.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Gemini 3 Flash Preview | 8.24 | 7.20 | 9.35 | 0.77 |
| 2 | GPT-5.4 | 8.02 | 6.15 | 9.60 | 1.24 |
| 3 | GPT-OSS-120B | 7.96 | 4.65 | 9.45 | 1.49 |
| 4 | DeepSeek V3 | 7.78 | 6.40 | 9.55 | 1.07 |
| 5 | Grok 4.20 | 7.62 | 5.40 | 8.80 | 1.07 |
| 6 | MiMo-V2-Flash | 7.26 | 5.05 | 8.80 | 1.22 |
| 7 | Claude Opus 4.6 | 7.17 | 4.65 | 9.00 | 1.64 |
| 8 | Claude Sonnet 4.6 | 6.47 | 2.65 | 8.60 | 1.84 |
| 9 | MiniMax M2.5 | 6.12 | 1.85 | 8.60 | 2.25 |
| 10 | Gemini 3.1 Pro | 4.84 | 1.85 | 7.80 | 1.97 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 4.45 |
| 2 | GPT-OSS-120B | 6.33 |
| 3 | Claude Opus 4.6 | 6.44 |
| 4 | Gemini 3.1 Pro | 6.51 |
| 5 | MiniMax M2.5 | 6.82 |
| 6 | MiMo-V2-Flash | 7.72 |
| 7 | Claude Sonnet 4.6 | 7.76 |
| 8 | Grok 4.20 | 7.87 |
| 9 | Gemini 3 Flash Preview | 8.68 |
| 10 | DeepSeek V3 | 8.76 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** deepseek_v4
**Total Judgments:** 100
**Valid Judgments:** 88

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

**Generation Time:** 27878ms
**Tokens:** 2117

```
Below is a practical GraphQL schema design for a social media platform with:

- Users
- Posts
- Comments
- Likes
- Follows

And it explicitly addresses:

- N+1 query problem via DataLoader
- Cursor-based pagination
- Proper input validation
- Rate limiting per field
- Real-time subscriptions
- Resolver implementations for the trickiest parts

I’ll use:

- GraphQL SDL
- Node.js/TypeScript-style resolver pseudocode
- Apollo-style conventions where helpful
- Relay-style connections for pagination

---

# 1. High-level design goals

A social media API usually needs to support:

- user profile lookups
- timelines/feed queries
- nested content trees
- counts and viewer-specific booleans like `viewerHasLiked`
- high write/read volumes
- real-time updates for posts/comments/likes

The tricky parts are usually:

1. Avoiding N+1 when resolving authors, likes, comments counts, etc.
2. Efficient pagination on feeds and comments
3. Validation for user-generated content
4. Rate-limiting expensive fields like feed/search
5. Subscription fanout and authorization

---

# 2. GraphQL schema (SDL)

```graphql
scalar DateTime
scalar Cursor
scalar JSON

directive @rateLimit(
  limit: Int!
  windowSeconds: Int!
  keyBy: RateLimitIdentity = USER
) on FIELD_DEFINITION

enum RateLimitIdentity {
  USER
  IP
}

enum SortOrder {
  ASC
  DESC
}

enum FeedType {
  HOME
  USER_POSTS
}

type Query {
  me: User

  user(id: ID!): User
  userByUsername(username: String!): User

  post(id: ID!): Post
  comment(id: ID!): Comment

  feed(
    type: FeedType = HOME
    userId: ID
    first: Int = 20
    after: Cursor
  ): PostConnection! @rateLimit(limit: 60, windowSeconds: 60, keyBy: USER)

  postComments(
    postId: ID!
    first: Int = 20
    after: Cursor
  ): CommentConnection! @rateLimit(limit: 120, windowSeconds: 60, keyBy: USER)

  userFollowers(
    userId: ID!
    first: Int = 20
    after: Cursor
  ): UserConnection! @rateLimit(limit: 60, windowSeconds: 60, keyBy: USER)

  userFollowing(
    u...
```

### Claude Opus 4.6

**Generation Time:** 37342ms
**Tokens:** 2122

```


# Social Media Platform - Production-Grade GraphQL Schema

## Complete Schema Definition

```graphql
# schema.graphql

# ============================================================
# CUSTOM SCALARS & DIRECTIVES
# ============================================================

scalar DateTime
scalar URL
scalar EmailAddress
scalar NonNegativeInt
scalar Cursor

"""Rate limit directive applied per field"""
directive @rateLimit(
  max: Int!
  window: String! # e.g., "1m", "1h", "1d"
  message: String
) on FIELD_DEFINITION

directive @auth(
  requires: Role = USER
) on FIELD_DEFINITION | OBJECT

directive @cacheControl(
  maxAge: Int
  scope: CacheControlScope
) on FIELD_DEFINITION | OBJECT

enum CacheControlScope {
  PUBLIC
  PRIVATE
}

enum Role {
  ADMIN
  MODERATOR
  USER
  GUEST
}

# ============================================================
# CONNECTION / PAGINATION TYPES (Relay-style)
# ============================================================

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: Cursor
  endCursor: Cursor
  totalCount: NonNegativeInt!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
}

type UserEdge {
  node: User!
  cursor: Cursor!
}

type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
}

type PostEdge {
  node: Post!
  cursor: Cursor!
}

type CommentConnection {
  edges: [CommentEdge!]!
  pageInfo: PageInfo!
}

type CommentEdge {
  node: Comment!
  cursor: Cursor!
}

type NotificationConnection {
  edges: [NotificationEdge!]!
  pageInfo: PageInfo!
}

type NotificationEdge {
  node: Notification!
  cursor: Cursor!
}

# ============================================================
# CORE TYPES
# ============================================================

type User {
  id: ID!
  username: String!
  email: EmailAddress! @auth(requires: ADMIN)
  displayName: String!
  bio: String
  avatarUrl: URL
  coverPhotoUrl: URL
  website: URL
  location: String
  isVerified: Boolean!
  isPri...
```

### Gemini 3.1 Pro

**Generation Time:** 35251ms
**Tokens:** 2107

```
Designing a robust, scalable GraphQL API for a social media platform requires careful attention to performance, security, and real-time capabilities. 

Below is a comprehensive solution encompassing the Schema Definition Language (SDL), DataLoader setup, and the resolver implementations for the most complex scenarios.

---

### 1. GraphQL Schema (SDL)

We use the **Relay Connection Specification** for cursor-based pagination and custom directives for rate limiting.

```graphql
# Custom Scalars & Directives
scalar DateTime
scalar Cursor

"""
Limits the invocation rate of a specific field per user/IP.
"""
directive @rateLimit(limit: Int!, duration: Int!) on FIELD_DEFINITION | MUTATION

# --- Interfaces & Shared Types ---
type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: Cursor
  endCursor: Cursor
}

# --- Types ---
type User {
  id: ID!
  username: String!
  bio: String
  createdAt: DateTime!
  
  # Paginated relationships
  posts(first: Int, after: Cursor): PostConnection!
  followers(first: Int, after: Cursor): UserConnection!
  following(first: Int, after: Cursor): UserConnection!
  
  # Computed fields
  followerCount: Int!
  followingCount: Int!
  isFollowedByMe: Boolean!
}

type Post {
  id: ID!
  author: User!
  content: String!
  mediaUrls: [String!]
  createdAt: DateTime!
  
  # Paginated relationships
  comments(first: Int, after: Cursor): CommentConnection!
  likedBy(first: Int, after: Cursor): UserConnection!
  
  # Computed fields
  likeCount: Int!
  commentCount: Int!
  isLikedByMe: Boolean!
}

type Comment {
  id: ID!
  post: Post!
  author:
```

### Claude Sonnet 4.6

**Generation Time:** 23490ms
**Tokens:** 2122

```
# GraphQL Social Media Platform - Complete Implementation

## Schema Definition

```graphql
# schema.graphql

scalar DateTime
scalar Cursor
scalar URL
scalar EmailAddress

# ─────────────────────────────────────────────
# Directives
# ─────────────────────────────────────────────

directive @auth(requires: Role = USER) on FIELD_DEFINITION | OBJECT
directive @rateLimit(
  max: Int!
  window: String!
  message: String
) on FIELD_DEFINITION
directive @validate(
  minLength: Int
  maxLength: Int
  pattern: String
  min: Float
  max: Float
) on INPUT_FIELD_DEFINITION | ARGUMENT_DEFINITION
directive @deprecated(reason: String) on FIELD_DEFINITION | ENUM_VALUE
directive @complexity(value: Int!, multipliers: [String!]) on FIELD_DEFINITION

enum Role {
  GUEST
  USER
  MODERATOR
  ADMIN
}

enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
  DELETED
}

enum NotificationType {
  LIKE
  COMMENT
  FOLLOW
  MENTION
  REPOST
}

enum ReactionType {
  LIKE
  LOVE
  HAHA
  WOW
  SAD
  ANGRY
}

enum SortOrder {
  ASC
  DESC
}

enum PostSortField {
  CREATED_AT
  LIKES_COUNT
  COMMENTS_COUNT
  RELEVANCE
}

# ─────────────────────────────────────────────
# Connection / Pagination Types
# ─────────────────────────────────────────────

interface Node {
  id: ID!
}

interface Connection {
  pageInfo: PageInfo!
  totalCount: Int!
}

interface Edge {
  cursor: Cursor!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: Cursor
  endCursor: Cursor
}

# ─────────────────────────────────────────────
# Core Types
# ─────────────────────────────────────────────

type User implements Node {
  id: ID!
  username: String!
  displayName: String!
  email: EmailAddress! @auth(requires: ADMIN)
  bio: String
  avatarUrl: URL
  coverUrl: URL
  isVerified: Boolean!
  isPrivate: Boolean!
  role: Role!
  createdAt: DateTime!
  updatedAt: DateTime!

  # Computed fields with DataLoader
  postsCount: Int!
  followersCount: Int!
  followingCount: Int!
  isFollowedByMe: Boolean! @a...
```

### Grok 4.20

**Generation Time:** 8697ms
**Tokens:** 2233

```
**GraphQL Schema for a Social Media Platform**

```graphql
# ==================== SCALARS & DIRECTIVES ====================

scalar DateTime
scalar Cursor

"""
Custom directive for rate limiting
"""
directive @rateLimit(
  max: Int! = 100
  window: String! = "1m"
  key: String = "ip"
) on FIELD_DEFINITION

"""
Custom directive for input validation
"""
directive @validate(
  regex: String
  min: Int
  max: Int
  required: Boolean = false
) on INPUT_FIELD_DEFINITION | ARGUMENT_DEFINITION

# ==================== TYPES ====================

type User {
  id: ID!
  username: String!
  email: String!
  displayName: String
  bio: String
  avatarUrl: String
  createdAt: DateTime!
  updatedAt: DateTime!

  # Connections
  posts(first: Int = 20, after: Cursor): PostConnection!
  followers(first: Int = 20, after: Cursor): UserConnection!
  following(first: Int = 20, after: Cursor): UserConnection!
  likes(first: Int = 20, after: Cursor): LikeConnection!
  
  isFollowing: Boolean!
  followerCount: Int!
  followingCount: Int!
  postCount: Int!
}

type Post {
  id: ID!
  content: String!
  imageUrls: [String!]
  author: User!
  createdAt: DateTime!
  updatedAt: DateTime!

  comments(first: Int = 20, after: Cursor): CommentConnection!
  likes(first: Int = 20, after: Cursor): LikeConnection!
  likeCount: Int!
  commentCount: Int!
  isLikedByMe: Boolean!
}

type Comment {
  id: ID!
  content: String!
  author: User!
  post: Post!
  parent: Comment
  createdAt: DateTime!
  updatedAt: DateTime!

  replies(first: Int = 10, after: Cursor): CommentConnection!
  likeCount: Int!
  isLikedByMe: Boolean!
}

type Like {
  id: ID!
  user: User!
  post: Post
  comment: Comment
  createdAt: DateTime!
}

# ==================== CONNECTIONS (Cursor-based Pagination) ====================

type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
}

type CommentConnection {
  edges: [CommentEdge!]!
  pageInfo: PageInfo!
}

t...
```

### DeepSeek V3

**Generation Time:** 141867ms
**Tokens:** 3567

```
# GraphQL Schema for Social Media Platform

Here's a comprehensive GraphQL schema design for a social media platform with optimizations for performance and scalability:

## Schema Definition

```graphql
scalar DateTime
scalar Upload

directive @rateLimit(
  max: Int
  window: String
  message: String
) on FIELD_DEFINITION

type Query {
  me: User!
  user(id: ID!): User
  post(id: ID!): Post
  feed(
    first: Int = 10
    after: String
    orderBy: FeedOrderBy = NEWEST
  ): PostConnection!
  searchUsers(
    query: String!
    first: Int = 10
    after: String
  ): UserConnection!
}

type Mutation {
  # User operations
  signUp(input: SignUpInput!): AuthPayload!
  login(input: LoginInput!): AuthPayload!
  updateProfile(input: UpdateProfileInput!): User!
  followUser(userId: ID!): FollowResult!
  unfollowUser(userId: ID!): FollowResult!
  
  # Post operations
  createPost(input: CreatePostInput!): Post!
  updatePost(id: ID!, input: UpdatePostInput!): Post!
  deletePost(id: ID!): Boolean!
  
  # Comment operations
  addComment(input: AddCommentInput!): Comment!
  updateComment(id: ID!, input: UpdateCommentInput!): Comment!
  deleteComment(id: ID!): Boolean!
  
  # Like operations
  likePost(postId: ID!): LikeResult!
  unlikePost(postId: ID!): LikeResult!
  likeComment(commentId: ID!): LikeResult!
  unlikeComment(commentId: ID!): LikeResult!
  
  # File upload
  uploadMedia(file: Upload!): Media!
}

type Subscription {
  postCreated: Post!
  postUpdated: Post!
  postDeleted: ID!
  commentAdded(postId: ID!): Comment!
  likeAdded(postId: ID!): Like!
  userFollowed(userId: ID!): Follow!
}

# Types
type AuthPayload {
  token: String!
  user: User!
}

type User {
  id: ID!
  username: String!
  email: String!
  name: String
  bio: String
  avatar: String
  posts(
    first: Int = 10
    after: String
  ): PostConnection!
  followers(
    first: Int = 10
    after: String
  ): UserConnection!
  following(
    first: Int = 10
    after: String
  ): UserConnection!
  likes(
  ...
```

### GPT-OSS-120B

**Generation Time:** 5714ms
**Tokens:** 2182

```
Below is a **complete, production‑ready GraphQL design** for a typical social‑media platform that includes:

| Feature | How it is addressed |
|---------|----------------------|
| **Core entities** | `User`, `Post`, `Comment`, `Like`, `Follow` |
| **N+1 problem** | Centralised **DataLoader** instances per request (users, posts, comments, likes, follows) |
| **Cursor‑based pagination** | `Connection` pattern (`edges`, `node`, `cursor`, `pageInfo`) on `Post` and `Comment` listings |
| **Input validation** | Custom scalars (`Email`, `URL`, `DateTime`) + **Joi**‑based validation in resolvers |
| **Rate limiting per field** | `graphql-rate-limit` directive (`@rateLimit(limit: X, duration: Y)`) |
| **Real‑time updates** | **Subscriptions** for new posts, new comments, likes, follows |
| **Tech stack** | Apollo Server 4 (Node ≥ 18), TypeScript, `dataloader`, `graphql-rate-limit`, `graphql-subscriptions`, `Joi` |

---

## 1. Schema (SDL)

```graphql
# -------------------------------------------------
#  Scalars
# -------------------------------------------------
scalar DateTime
scalar Email
scalar URL

# -------------------------------------------------
#  Directives
# -------------------------------------------------
directive @rateLimit(
  limit: Int!          # max calls
  duration: Int!       # seconds window
) on FIELD_DEFINITION

# -------------------------------------------------
#  Pagination Types (Relay style)
# -------------------------------------------------
type PageInfo {
  startCursor: String
  endCursor: String
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
}

interface Edge {
  cursor: String!
}

# -------------------------------------------------
#  Core Types
# -------------------------------------------------
type User {
  id: ID!
  username: String!
  email: Email!
  avatar: URL
  bio: String
  createdAt: DateTime!
  followers(first: Int, after: String): FollowConnection!
  following(first: Int, after: String): FollowConnection!
  posts(first: Int...
```

### Gemini 3 Flash Preview

**Generation Time:** 13042ms
**Tokens:** 1680

```
This design addresses the complexities of a modern social media backend, focusing on performance, scalability, and developer experience.

### 1. The GraphQL Schema (`schema.graphql`)

We use **Directives** for rate limiting and **Cursor-Based Pagination** (Relay spec) for performance.

```graphql
directive @rateLimit(limit: Int, duration: Int) on FIELD_DEFINITION

type Query {
  # Cursor-based pagination for global feed
  feed(first: Int, after: String): PostConnection! @rateLimit(limit: 100, duration: 60)
  user(id: ID!): User
  me: User
}

type Mutation {
  createPost(input: CreatePostInput!): Post! @rateLimit(limit: 5, duration: 60)
  toggleLike(postId: ID!): LikePayload!
  followUser(userId: ID!): FollowPayload!
}

type Subscription {
  postCreated: Post!
  newComment(postId: ID!): Comment!
}

type User {
  id: ID!
  username: String!
  email: String!
  posts(first: Int, after: String): PostConnection!
  followersCount: Int!
  followingCount: Int!
  # Relationship tracking
  isFollowing: Boolean! 
}

type Post {
  id: ID!
  content: String!
  author: User!
  likesCount: Int!
  comments(first: Int, after: String): CommentConnection!
  createdAt: String!
}

# Relay-style Pagination Types
type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
}

type PostEdge {
  cursor: String!
  node: Post!
}

type PageInfo {
  hasNextPage: Boolean!
  endCursor: String
}

input CreatePostInput {
  content: String! @constraint(minLength: 1, maxLength: 280)
}
```

---

### 2. Solving N+1 with DataLoaders

The "N+1" problem occurs when fetching a list of posts and then fetching the author for each post individually. We use `dataloader` to batch these into a single SQL `IN` query.

**DataLoader Setup (`context.js`):**
```javascript
import DataLoader from 'dataloader';

export const createLoaders = (db) => ({
  userLoader: new DataLoader(async (userIds) => {
    // Single query: SELECT * FROM users WHERE id IN (...)
    const users = await db.table('users').whereIn('id', us...
```

### MiniMax M2.5

**Generation Time:** 76286ms
**Tokens:** 2149

```
This is a comprehensive design for a social media GraphQL API. It uses **Apollo Server** (Node.js) as the implementation context, as it is the industry standard, but the concepts apply to any language.

### 1. The Schema (SDL)

We will use **Cursor-based pagination** (Relay specification style) to handle large datasets efficiently and stably.

```graphql
scalar DateTime

# --- Types ---

type User {
  id: ID!
  username: String!
  email: String! @auth # Custom directive or resolved via context
  bio: String
  avatarUrl: String
  followersCount: Int!
  followingCount: Int!
  createdAt: DateTime!
  # Relationships
  posts(limit: Int): [Post!]!
  following: [User!]!
  followers: [User!]!
}

type Post {
  id: ID!
  content: String!
  author: User!
  likesCount: Int!
  commentsCount: Int!
  createdAt: DateTime!
  # Complex: Pagination for comments
  comments(first: Int, after: String): CommentConnection!
  # Complex: Did the current user like this?
  viewerHasLiked: Boolean!
}

type Comment {
  id: ID!
  content: String!
  author: User!
  post: Post!
  createdAt: DateTime!
}

type Like {
  id: ID!
  user: User!
  post: Post!
  createdAt: DateTime!
}

# --- Pagination Connections (Relay Spec) ---

type PostEdge {
  node: Post!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  endCursor: String
}

type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
}

type CommentEdge {
  node: Comment!
  cursor: String!
}

type CommentConnection {
  edges: [CommentEdge!]!
  pageInfo: PageInfo!
}

# --- Inputs ---

input CreatePostInput {
  content: String! # Validation: Length 1-500
}

input CreateCommentInput {
  postId: ID!
  content: String!
}

input FollowUserInput {
  userId: ID!
}

# --- Root Query ---

type Query {
  # The Feed for the logged-in user
  timeline(first: Int, after: String): PostConnection! @rateLimit(limit: 10, window: "1m")
  
  # Fetch a specific user
  user(username: String!): User
  
  # Fetch a specific post
  post(id: ID!): Post
}

# ...
```

### MiMo-V2-Flash

**Generation Time:** 13596ms
**Tokens:** 2146

```
This is a comprehensive design for a social media GraphQL API using **Node.js**, **Apollo Server**, **Prisma ORM** (for database abstraction), and **Redis** (for pub/sub and caching).

### 1. Architecture Overview

*   **Database:** PostgreSQL (via Prisma).
*   **DataLoader:** Batched requests to the database to solve N+1.
*   **Pagination:** Cursor-based (Relay-style).
*   **Rate Limiting:** Field-level complexity analysis + fixed window counters.
*   **Real-time:** GraphQL Subscriptions over Redis Pub/Sub.

---

### 2. GraphQL Schema Definition (`schema.graphql`)

```graphql
scalar DateTime
scalar Cursor

# --- Enums ---
enum Role {
  USER
  ADMIN
}

enum SortOrder {
  ASC
  DESC
}

# --- Inputs ---
input PostInput {
  content: String!
  mediaUrl: String
}

input PaginationInput {
  first: Int @constraint(min: 1, max: 50)
  after: Cursor
  last: Int @constraint(min: 1, max: 50)
  before: Cursor
}

# --- Types ---
type User {
  id: ID!
  username: String!
  email: String!
  role: Role!
  createdAt: DateTime!
  
  # Relationships
  posts(first: Int, after: Cursor): PostConnection!
  followers(first: Int, after: Cursor): UserConnection!
  following(first: Int, after: Cursor): UserConnection!
  isFollowing: Boolean! # Context-aware field
}

type Post {
  id: ID!
  content: String!
  mediaUrl: String
  author: User!
  createdAt: DateTime!
  updatedAt: DateTime!
  
  # Aggregates (often heavy, optimized via DataLoader)
  likeCount: Int!
  commentCount: Int!
  
  # Relationships
  likes(first: Int, after: Cursor): LikeConnection!
  comments(first: Int, after: Cursor): CommentConnection!
  isLikedByMe: Boolean! # Context-aware field
}

type Comment {
  id: ID!
  content: String!
  author: User!
  post: Post!
  createdAt: DateTime!
}

type Like {
  id: ID!
  user: User!
  post: Post!
  createdAt: DateTime!
}

# --- Connections (Cursor-based Pagination) ---
type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: Cursor
  endCursor: Cursor
}

type ...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*