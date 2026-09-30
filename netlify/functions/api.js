const serverless = require('serverless-http');
const connectDB = require('../../config/db');
const app = require('../../server');

const serverlessHandler = serverless(app);

module.exports.handler = async (event, context) => {
  // Ensure connection to MongoDB is ready
  context.callbackWaitsForEmptyEventLoop = false;
  await connectDB();
  return await serverlessHandler(event, context);
};
