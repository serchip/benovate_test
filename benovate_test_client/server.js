var webpack = require('webpack')
var WebpackDevServer = require('webpack-dev-server')
var config = require('./webpack.local.config')

new WebpackDevServer(webpack(config), {
    publicPath: config.output.publicPath,
    hot: true,
    inline: true,
    historyApiFallback: true
}).listen(8090, '127.0.0.1', function (err, result) {
    if (err) {
        console.log(err)
    }

    console.log('Listening at 127.0.0.1:8090')
})