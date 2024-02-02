// Filters.jsx
import PropTypes from "prop-types";

const Filters = ({ selectedComponent, handleSelect }) => {
  return (
    <div
      id="filters"
      className={`col p-2 text-center border border-dark ${
        selectedComponent === "Filters" ? "selected" : ""
      }`}
      onClick={() => handleSelect("Filters")}
    >
      Filters
    </div>
  );
};

Filters.propTypes = {
  selectedComponent: PropTypes.string.isRequired,
  handleSelect: PropTypes.func.isRequired,
};

export default Filters;
