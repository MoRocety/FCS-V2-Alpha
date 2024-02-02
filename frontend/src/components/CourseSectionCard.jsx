import { useState } from "react";
import PropTypes from "prop-types";
import SectionCard from "./SectionCard";
import "./CourseSectionCard.css";

const CourseSectionCard = ({ course, sections, onSectionClick }) => {
  const { dept, course_code, course_name, course_credits } = course;
  const [isCollapsed, setIsCollapsed] = useState(true);

  const handleToggleCollapse = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    <div className={`card bg-dark text-white custom-section-card card2 small`}>
      <div className="card-header" id={`heading-${course_code}`}>
        <span className="mb-0 d-flex justify-content-between align-items-center">
          <button
            className={`btn p-0 btn-link ${isCollapsed ? "" : "collapsed"}`}
            type="button"
            onClick={handleToggleCollapse}
            aria-expanded={isCollapsed ? "true" : "false"}
            aria-controls={`collapse-${course_code}`}
          >
            <i className={`fas fa-chevron-${isCollapsed ? "down" : "up"}`}></i>{" "}
            {`${dept} ${course_code} - ${course_name}`}
          </button>
          <span>Credits: {course_credits}</span>
        </span>
      </div>

      <div
        id={`collapse-${course_code}`}
        className={`collapse ${isCollapsed ? "" : "show"}`}
        aria-labelledby={`heading-${course_code}`}
      >
        <div className="card-body">
          {sections.map((section) => (
            <SectionCard
              key={section.id}
              section={section}
              onBgColorChange={(sectionId, isSelected) =>
                onSectionClick(sectionId, isSelected)
              }
            />
          ))}
        </div>
      </div>
    </div>
  );
};

CourseSectionCard.propTypes = {
  course: PropTypes.shape({
    dept: PropTypes.string.isRequired,
    course_code: PropTypes.string.isRequired,
    course_name: PropTypes.string.isRequired,
    course_credits: PropTypes.number.isRequired,
  }).isRequired,
  sections: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
    })
  ).isRequired,
  onSectionClick: PropTypes.func.isRequired, // Add prop type for handling section clicks
};

export default CourseSectionCard;
