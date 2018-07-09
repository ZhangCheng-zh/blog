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

// set cookie
app.use(async function(ctx, next) {
  const n = ~~ctx.cookies.get('view') + 1;
  ctx.cookies.set('view', n);
  ctx.body = n + ' views';

  if (ctx.url === '/index') {
    ctx.cookies.set(
      'cid',
      'hello world',
      {
        domain: 'localhost',  // 写cookie所在的域名
        path: '/index',       // 写cookie所在的路径
        // maxAge: 10 * 60 * 1000, // cookie有效时长
        // expires: new Date('2018-09-15'),  // cookie失效时间
        httpOnly: false,  // 是否只用于http请求中获取
        overwrite: false,  // 是否允许重写，
        secure: true
      }
    )
  }
  next();
});

// response
app.use(async (ctx) => {

  await setTimeout(() => {}, 1000);

});



// error handler
app.on('error', (err) => {
  if (process.env.NODE_ENV !== 'test') {
    console.log(err.message || 'Something Error!');
  }
});

app.console
app.listen(3000, () => {
  console.log('[demo] cookie is starting at port 3000')
});
