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

-- create partitions by month
create table posts (
    id serial,
    user_id int,
    content text,
    created_at timestamp
) partition by range(created_at);

create table posts_2024_1 partition of posts 
for values from ('2024-01-01') to ('2024-02-01')


"""
Wnen a write occurs in PostgreSQL, several steps happen to ensure both performance
and durability
1 Transaction Log(WAL) Write[DISK]
2 Buffer Cache Update[memory]
3 Background Write[Memory -> Disk]
4 Index Updates [Memory & Disk]

What affects throughput limits? several factors:
1 Hardwar: write throughput is often bottlenecked by disk I/O for the WAL
2 Indexes: each additional index reduces write throughput
3 Replication: If configured, synchronous replication add latency as we wait for replicas to comfirm
4 Transaction complexity: more tables or indexes touched = slower transactions

Write performance optimization
1 Vertical scaling: Using faster NVM disks for better WAL performance, adding more RAM to increase the buffer cache size,
or upgrading to CPUs with more cores tp handle parallel operations more effectively
2 Batch processing: instead of processing each write individually, collect multiple operations and execute them in a single
transaction.
3 Write offloading: using message queue to decouple producer and consumer
4 Table partitioning: 
5 Sharding
"""