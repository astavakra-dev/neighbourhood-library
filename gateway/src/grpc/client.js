const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");
const path = require("path");
const { grpcHost } = require("../config/gateway.config");

const PROTO_PATH = path.join(__dirname, "../../proto/library_service.proto");

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});

const libraryProto = grpc.loadPackageDefinition(packageDefinition).library;

const client = new libraryProto.LibraryService(grpcHost, grpc.credentials.createInsecure());

module.exports = client;