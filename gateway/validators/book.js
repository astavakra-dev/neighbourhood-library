const Joi = require('joi');

const bookSchema = Joi.object({
  title: Joi.string().min(1).required(),
  author: Joi.string().min(1).required(),
  published_year: Joi.number().integer().min(0).required()
});

module.exports = { bookSchema };