import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import BooksPage from "./pages/BooksPage";
import MembersPage from "./pages/MembersPage";
import BorrowPage from "./pages/BorrowPage";

export default function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/books">Books</Link> | 
        <Link to="/members">Members</Link> | 
        <Link to="/borrow">Borrow</Link>
      </nav>
      <Routes>
        <Route path="/books" element={<BooksPage />} />
        <Route path="/members" element={<MembersPage />} />
        <Route path="/borrow" element={<BorrowPage />} />
      </Routes>
    </BrowserRouter>
  );
}