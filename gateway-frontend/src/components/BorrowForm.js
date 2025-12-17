import { useState } from "react";
import { borrowBook, returnBook } from "../api/borrow";

export default function BorrowForm() {
  const [bookId, setBookId] = useState("");
  const [memberId, setMemberId] = useState("");

  const handleBorrow = async () => {
    try {
      const record = await borrowBook({ book_id: parseInt(bookId), member_id: parseInt(memberId) });
      alert(`Borrowed record id: ${record.record_id}`);
    } catch {
      alert("Borrow failed");
    }
  };

  const handleReturn = async () => {
    try {
      const result = await returnBook({ book_id: parseInt(bookId), member_id: parseInt(memberId) });
      alert(`Return success: ${result.success}`);
    } catch {
      alert("Return failed");
    }
  };

  return (
    <div>
      <input placeholder="Book ID" value={bookId} onChange={e => setBookId(e.target.value)} />
      <input placeholder="Member ID" value={memberId} onChange={e => setMemberId(e.target.value)} />
      <button onClick={handleBorrow}>Borrow</button>
      <button onClick={handleReturn}>Return</button>
    </div>
  );
}