import React, { useState } from "react";
import axios from "axios";
import "./UploadForm.css";

export default function UploadForm() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://localhost:8000/parse_resume/",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      setResults(response.data);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  const renderSection = (title, items) => {
    if (!items || items.length === 0) return null;

    return (
      <div className="section-card">
        <h2>{title}</h2>
        <ul>
          {title === "Profile" && items.length > 0
            ? items.map((line, idx) => (
                <li key={idx}>
                  {idx === 0 ? <strong>{line}</strong> : line}
                </li>
              ))
            : items.map((line, idx) => <li key={idx}>{line}</li>)}
        </ul>
      </div>
    );
  };

  return (
    <div className="container">
      <h1 className="title">Resume Parser</h1>

      <form onSubmit={handleSubmit} className="upload-form">
        <label className="custom-file-upload">
          {file ? file.name : "Choose Resume"}
          <input type="file" onChange={handleFileChange} />
        </label>
        <button type="submit">Upload Resume</button>
      </form>

      {results && (
        <div className="results">
          {renderSection("Profile", results.profile)}
          {renderSection("Objective", results.objective)}
          {renderSection("Education", results.education)}
          {renderSection("Experience", results.experience)}
          {renderSection("Skills", results.skills)}
          {renderSection("Projects", results.projects)}
        </div>
      )}
    </div>
  );
}
