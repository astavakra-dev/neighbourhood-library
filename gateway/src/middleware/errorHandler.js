// Fallback error handler for unexpected runtime errors
module.exports = function errorHandler(err, req, res, next) {
  // If error was already handled (has status), send it
  if (res.headersSent) return next(err);
  console.error("Unhandled error:", err);
  res.status(500).json({ error: "Internal error", details: "Unexpected server error" });
};