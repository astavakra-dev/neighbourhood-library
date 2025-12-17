const validate = (schema) => (req, res, next) => {
  const payload = ["GET", "DELETE"].includes(req.method) ? req.query : req.body;
  const { error, value } = schema.validate(payload, { abortEarly: false, stripUnknown: true });
  if (error) {
    return res.status(400).json({
      error: "Invalid input",
      details: error.details.map(d => ({ message: d.message, path: d.path }))
    });
  }
  if (["GET", "DELETE"].includes(req.method)) req.query = value;
  else req.body = value;
  next();
};

module.exports = validate;