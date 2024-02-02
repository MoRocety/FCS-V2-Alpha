import PropTypes from "prop-types";
import axios from "axios";
import "./CourseCard.css";

const CourseCard = ({
  course,
  isSelected,
  handleAddCourse,
  handleRemoveCourse,
  onCourseDataReceived,
}) => {
  const header = `${course.dept} ${course.course_code}`;

  const handleAddClick = async () => {
    try {
      const response = await axios.get(
        "http://localhost:8000/api/add_course/",
        {
          params: {
            id: course.id,
          },
        }
      );
      console.log("Course sent to backend for addition:", course);

      // Call the callback function to pass the received data to the parent component
      onCourseDataReceived(response.data);

      // Call handleAddCourse to update the course list in the parent component
      handleAddCourse(course.id);
    } catch (error) {
      console.error("Error sending course to backend for addition:", error);
    }
  };

  const handleRemoveClick = () => {
    // Call handleRemoveCourse to remove the course from the list in the parent component
    handleRemoveCourse(course.id);
  };

  return (
    <div
      className={`card bg-dark text-white custom-card ${
        isSelected ? "border-success" : ""
      }`}
      onClick={isSelected ? handleRemoveClick : handleAddClick} // Toggle between adding and removing course
    >
      <div className="card-header d-flex justify-content-between">
        <span className="card-text m-0 small">
          {header} - {course.course_name}
        </span>
        <span className="card-text m-0 small">
          Credits: {course.course_credits}
        </span>
      </div>
    </div>
  );
};

CourseCard.propTypes = {
  course: PropTypes.shape({
    id: PropTypes.number.isRequired,
    course_code: PropTypes.string.isRequired,
    course_name: PropTypes.string.isRequired,
    course_credits: PropTypes.number.isRequired,
    dept: PropTypes.string.isRequired,
  }).isRequired,
  isSelected: PropTypes.bool.isRequired,
  handleAddCourse: PropTypes.func.isRequired,
  handleRemoveCourse: PropTypes.func.isRequired, // Add prop type for removing course
  onCourseDataReceived: PropTypes.func.isRequired,
};

export default CourseCard;
