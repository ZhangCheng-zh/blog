const Koa = require('koa');

const app = new Koa();

// x-response-time

app.use(async (ctx, next) => {
  const start = Date.now();

  await next();

  const ms = Date.now() - start;
  ctx.set('X-Response-Time', `${ms}ms`);
});

// logger

app.use(async (ctx, next) => {
  const start = Date.now();

  await next();

  const ms = Date.now() - start;

  console.log(`${ctx.method} ${ctx.url} - ${ms}`);
});

// response

app.use(async (ctx) => {
  ctx.body = 'Hello World';

  await setTimeout(() => {}, 1000);
});

// error handler
app.on('error', (err) => {
  if (process.env.NODE_ENV !== 'test') {
    console.log(err.message || 'Something Error!');
  }
});

app.listen(3000);
