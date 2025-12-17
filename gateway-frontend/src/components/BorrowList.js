import { useState } from "react";
import { listBorrowedBooks } from "../api/borrow";

export default function BorrowList() {
  const [memberId, setMemberId] = useState("");
  const [books, setBooks] = useState([]);

  const handleFetch = async () => {
    try {
      const result = await listBorrowedBooks(parseInt(memberId));
      setBooks(result.books || []);
    } catch {
      alert("Fetch failed");
    }
  };

  return (
    <div>
      <input placeholder="Member ID" value={memberId} onChange={e => setMemberId(e.target.value)} />
      <button onClick={handleFetch}>List Borrowed Books</button>
      <ul>
        {books.map((b, i) => <li key={i}>{b.title}</li>)}
      </ul>
    </div>
  );
}