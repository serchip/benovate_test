const webpack = require('webpack');
const ExtractTextPlugin = require("extract-text-webpack-plugin");
var BundleTracker = require('webpack-bundle-tracker')

module.exports = {
    entry: [
        //'react-hot-loader/patch',
        'webpack-dev-server/client?http://127.0.0.1:8090',
        'webpack/hot/only-dev-server',
        "./src/main.js"

    ],
    output: {
        path: __dirname + '/public/build/',
        publicPath: "http://127.0.0.1:8090/build/",
        filename: "bundle.js"
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                loader: "babel-loader",
                exclude: [/node_modules/, /public/],
                query:
                {
                    presets:['react']
                }
            },
            {
                test: /\.css$/,
                use: ExtractTextPlugin.extract({
                    fallback: "style-loader",
                    use: ["css-loader", 'autoprefixer-loader']
                }),
                exclude: [/node_modules/, /public/]
            },
            {
                test: /\.gif$/,
                loader: "url-loader?limit=10000&mimetype=image/gif"
            },
            {
                test: /\.jpg$/,
                loader: "url-loader?limit=10000&mimetype=image/jpg"
            },
            {
                test: /\.png$/,
                loader: "url-loader?limit=10000&mimetype=image/png"
            },
            {
                test: /\.svg/,
                loader: "url-loader?limit=26000&mimetype=image/svg+xml"
            },
            {
                test: /\.jsx$/,
                loader: "babel-loader",
                exclude: [/node_modules/, /public/],
                query:
                {
                    presets:['react']
                }
            },
            {
                test: /\.json$/,
                loader: "json-loader"
            }
        ]
    },
    plugins: [
        new ExtractTextPlugin("styles.css"),
        // enable HMR globally
        new webpack.HotModuleReplacementPlugin(),
        //new webpack.NoErrorsPlugin(), // don't reload if there is an error

        new BundleTracker({filename: './webpack-stats.json'}),
        // prints more readable module names in the browser console on HMR updates
        new webpack.NamedModulesPlugin(),
    ]
}
