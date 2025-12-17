function mapGrpcError(err, res) {
  if (!err.code) {
    return res.status(500).json({ error: "Unknown error", details: err.message });
  }

  switch (err.code) {
    case 3: // INVALID_ARGUMENT
      return res.status(400).json({ error: "Invalid input", details: err.details });
    case 5: // NOT_FOUND
      return res.status(404).json({ error: "Not found", details: err.details });
    case 6: // ALREADY_EXISTS
      return res.status(409).json({ error: "Already exists", details: err.details });
    case 9: // FAILED_PRECONDITION
      return res.status(412).json({ error: "Precondition failed", details: err.details });
    default:
      return res.status(500).json({ error: "Internal error", details: err.details });
  }
}

module.exports = mapGrpcError;