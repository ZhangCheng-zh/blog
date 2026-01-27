--  DDL
-- create table
create table users (
    id serial primary key,
    email varchar(255) unique
);
-- alter table
alter table users add column username text;


-- DML Data manipulation language
-- find all users who joined in the last week
select * from users where created_at > now() - interval '7 days';

-- Update a user's email
update users set email = 'new@email.com' where id = 123;


-- DCL Data control permissions
-- grant revoke
grant select on users to read_only_user;

-- Below is a basic SQL learning guide using a Newsfeed system as the running example. 
-- I’ll use PostgreSQL-style SQL and camelCase identifiers to match your usual style.

-- A tiny newsfeed schema
-- user
create table users (
    userId    bigint      primary key,
    username  text        not null unique,
    createdAt timestamp   not null    default now()
)

-- follow graph
create table follows (
    followerId   bigint    not null,
    followeeId   bigint    not null,
    createdAt    timestamp not null default now(),
    primary key (followerId, followeeId),
    foreign key (followerId) references users(userId),
    foreign key (followeeId) references users(userId)
);

-- posts
create table posts (
    postId    bigint    primary key,
    authorId  bigint    not null references users(userId),
    content   text      not null,
    createdAt timestamp not null default now()
)

-- Fan-out (precomputed feed)
create table feedItems (
    userId   bigint  not null references users(userId),
    postId   bigint  not null references posts(postId),
    rankedAt timestamp not null default now(),
    primary key (userId, postId)
)


-- add index 
create index idxPostsAuthorCreatedAt on posts(authorId, createdAt DESC);
create index idxFeedItemsUserRankedAt on feedItems(userId, rankedAt DESC);

-- select
-- get user's profile
select userId, username, createdAt from users where userId = 42;

-- get latest posts by one author
select postId, content, createdAt 
from posts 
where authorId = 42 
order by createAt DESC 
limit 20;

-- latest 100 posts from all followees
select p.postId, p.authorId, p.content, p.createdAt 
from follows f 
join posts p 
on p.authorId = f.followeeId
where f.followerId = :userId
order by p.createdAt DESC, p.postId DESC
LIMIT 100;

-- pagination
-- offset pagination
select postId, authorId, createAt
from posts
order by createdAt DESC
limit 20 offset 40;

-- keyset pagination
select postId, authorId, createdId
from posts
where createdAt < :lastCreatedAt
order by createdAt DESC
limit 20;