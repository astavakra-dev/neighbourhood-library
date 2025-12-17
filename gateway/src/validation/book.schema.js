const Joi = require("joi");

const addBookSchema = Joi.object({
  title: Joi.string().trim().min(1).max(200).required(),
  author: Joi.string().trim().min(1).max(120).required(),
  published_year: Joi.number().integer().min(1450).max(new Date().getFullYear()).required()
});

const updateBookSchema = Joi.object({
  id: Joi.number().integer().positive().required(),
  title: Joi.string().trim().min(1).max(200).required(),
  author: Joi.string().trim().min(1).max(120).required(),
  published_year: Joi.number().integer().min(1450).max(new Date().getFullYear()).required()
});

module.exports = { addBookSchema, updateBookSchema };