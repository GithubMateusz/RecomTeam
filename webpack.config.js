const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const path = require('path');
const WebpackConcatPlugin = require('webpack-concat-files-plugin');

module.exports = {
    context: __dirname,
    entry: './static/js/app.js',
    output: {
        filename: "app.js?[hash]",
        path: path.resolve(__dirname, 'static/bundles/'),
        publicPath: "bundles/"
    },
    module: {
        rules: [
            {
                test: /\.(scss)$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: 'css-loader',
                        options: {
                            url: false,
                        },
                    },
                    'sass-loader'
                ]
            },
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: ['babel-loader']
            }
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: '/app.css?[hash]',
        }),
        new WebpackConcatPlugin({
            bundles: [
                {
                    dest: './dist/app.js',
                    src: './static/js/**/*.js',
                },

            ],

        })
    ]
}
