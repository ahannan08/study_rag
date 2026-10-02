import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider } from "@/context/AuthContext";
import { DemoDocumentPage } from "@/pages/DemoDocumentPage";
import { DemoLibraryPage } from "@/pages/DemoLibraryPage";
import { DocumentPage } from "@/pages/DocumentPage";
import { HomePage } from "@/pages/HomePage";
import { LibraryPage } from "@/pages/LibraryPage";
import { LoginPage } from "@/pages/LoginPage";
import { RegisterPage } from "@/pages/RegisterPage";
import { ReviewPage } from "@/pages/ReviewPage";
import { ProtectedRoute } from "@/routes/ProtectedRoute";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/demo" element={<DemoLibraryPage />} />
          <Route path="/demo/documents/:documentId" element={<DemoDocumentPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/app" element={<LibraryPage />} />
            <Route path="/app/documents/:documentId" element={<DocumentPage />} />
            <Route path="/app/review" element={<ReviewPage />} />
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
