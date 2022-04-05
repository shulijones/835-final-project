module.exports = {
  devServer: {
    proxy: {
      "/api": { 
        // say front end server is running on localhost:8080; 
        // any call to localhost:8080/api/whatever will be redirected
        // to localhost:5000/whatever (without any CORS issues!)
        target: "http://localhost:5000",
        changeOrigin: true,
        logLevel: "debug",
        pathRewrite: { "/api": "/" }
      }
    }
  }
};
