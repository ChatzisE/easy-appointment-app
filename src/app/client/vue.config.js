const path = require("path");
const settings = {
    outputDir: path.resolve(__dirname, '../static'),
    devServer: {
        proxy: {
            '/': {
                target: 'http://localhost:8000/',
                ws: false,
            }
        }
    },
    configureWebpack: {
        devtool: 'source-map',
        plugins: [],
    }
};
if (process.env.NODE_ENV === 'production') {
    console.log("production")
    //--Not to generate source maps
    settings.productionSourceMap = false;
}
module.exports = settings;