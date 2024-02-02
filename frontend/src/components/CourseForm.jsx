// CourseForm.jsx

import { useState } from "react";
import PropTypes from "prop-types";
import axios from "axios";
import "./CourseForm.css";

const CourseForm = ({ handleCoursesData }) => {
  const [inputValue, setInputValue] = useState("");

  const handleInputChange = async (event) => {
    const { value } = event.target;
    setInputValue(value.toUpperCase());
    try {
      const response = await axios.get(
        // Change POST to GET
        "http://localhost:8000/api/retrieve_courses/",
        {
          params: {
            course: value.toUpperCase(),
          },
        }
      );
      // Pass the retrieved data to the parent component
      handleCoursesData(response.data);
    } catch (error) {
      console.error("Error retrieving data:", error);
      // Pass an empty array if there's an error
      handleCoursesData([]);
    }
  };

  return (
    <div className="form-group">
      <input
        type="text"
        className="form-control bg-dark text-white input-field"
        placeholder="DEPT 000X"
        value={inputValue}
        onChange={handleInputChange}
      />
    </div>
  );
};

CourseForm.propTypes = {
  handleCoursesData: PropTypes.func.isRequired,
};

export default CourseForm;
