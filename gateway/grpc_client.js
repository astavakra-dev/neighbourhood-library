const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

// Load proto definition
const PROTO_PATH = path.join(__dirname, 'proto', 'library_service.proto');
const packageDef = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});

const proto = grpc.loadPackageDefinition(packageDef).library.v1;

// Create client instance
const client = new proto.LibraryService(
  "localhost:50051", // Python gRPC server address
  grpc.credentials.createInsecure()
);

module.exports = client;