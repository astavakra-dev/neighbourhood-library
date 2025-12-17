import axios from "axios";

const BASE_URL = "http://localhost:3000";

export const borrowBook = async (payload) => {
  const res = await axios.post(`${BASE_URL}/borrow`, payload);
  return res.data;
};

export const returnBook = async (payload) => {
  const res = await axios.post(`${BASE_URL}/borrow/return`, payload);
  return res.data;
};

export const listBorrowedBooks = async (memberId) => {
  const res = await axios.get(`${BASE_URL}/borrow/${memberId}`);
  return res.data;
};