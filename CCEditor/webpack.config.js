const path = require('path');

module.exports = function (env, argv) {
    return {
        entry: './js/cceditor.js',
        output: {
            path: path.resolve(__dirname, 'dist'),
            filename: 'cceditor.bundle.js'
        },
        mode: env.production ? 'production' : 'development',
        devtool: env.production ? 'source-maps' : 'eval'
    };
};
