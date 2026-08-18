module.exports = {
  apps: [
    {
      name: "portfolio",
      script: "node_modules/.bin/serve",
      args: "-s dist -l 4321",
      cwd: __dirname,
      env: {
        NODE_ENV: "production",
      },
    },
  ],
};
