import { useState } from "react";
import PropTypes from "prop-types";

const SectionCard = ({ section, onBgColorChange }) => {
  const [isSelected, setIsSelected] = useState(true);

  const toggleSelection = () => {
    const updatedValue = !isSelected;
    setIsSelected(updatedValue);
    onBgColorChange(section.id, updatedValue); // Pass the updated isSelected value
  };

  return (
    <div
      className={`card ${
        isSelected ? "bg-success" : "bg-danger"
      } text-white mb-3`}
      onClick={toggleSelection}
    >
      <div className="card-body m-0">
        <p className="card-title m-0 text-white">
          Section {section.section_id}
          {/* Conditionally render instructor if available */}
          {section.instructor && (
            <span className="text-white"> by {section.instructor}</span>
          )}
        </p>

        {/* Conditionally render location, days, start/end time together if location exists */}
        {section.location && (
          <p className="card-text m-0 text-white">
            {section.location} at {section.section_days} from{" "}
            {section.start_time} to {section.end_time}
          </p>
        )}

        {/* Render alternate details if they exist */}
        {section.alt_location && (
          <p className="card-text m-0 text-white">
            {section.alt_location} at {section.alt_days} from{" "}
            {section.alt_start_time} to {section.alt_end_time}
          </p>
        )}
      </div>
    </div>
  );
};

SectionCard.propTypes = {
  section: PropTypes.shape({
    id: PropTypes.number.isRequired,
    section_id: PropTypes.string.isRequired,
    location: PropTypes.string,
    instructor: PropTypes.string,
    start_time: PropTypes.string,
    end_time: PropTypes.string,
    section_days: PropTypes.string,
    alt_location: PropTypes.string,
    alt_start_time: PropTypes.string,
    alt_end_time: PropTypes.string,
    alt_days: PropTypes.string,
  }).isRequired,
  onBgColorChange: PropTypes.func.isRequired, // Callback function to handle bg color change
};

export default SectionCard;
