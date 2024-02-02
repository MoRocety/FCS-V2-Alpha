import PropTypes from "prop-types";

const Advanced = ({ selectedComponent, handleSelect }) => {
  const handleClick = () => {
    // Only call handleSelect if the selectedComponent is not already "Advanced"
    if (selectedComponent !== "Advanced") {
      handleSelect("Advanced");
    }
  };

  return (
    <div
      id="advanced"
      className={`col p-2 text-center border border-dark ${
        selectedComponent === "Advanced" ? "selected" : ""
      } ${selectedComponent === "Advanced" ? "" : "disabled"}`}
      onClick={handleClick}
      tabIndex={selectedComponent === "Advanced" ? 0 : -1} // Add tabIndex to disable click event for accessibility
      aria-disabled={selectedComponent !== "Advanced"} // Add aria-disabled attribute for accessibility
    >
      Advanced
    </div>
  );
};

Advanced.propTypes = {
  selectedComponent: PropTypes.string.isRequired,
  handleSelect: PropTypes.func.isRequired,
};

export default Advanced;
