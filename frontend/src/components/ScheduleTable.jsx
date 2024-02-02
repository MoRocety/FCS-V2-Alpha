import PropTypes from "prop-types";
import "./ScheduleTable.css";

const colors = [
  "#9DF4F2",
  "#CAFA9B",
  "#7C99F5",
  "#E8A3F7",
  "#B5D6F6",
  "#C4FAFE",
  "#EAB2A0",
  "#F092A7",
  "#BDF29F",
  "#88C7DD",
  "#FAE4A0",
];

function ScheduleTable({ combinations }) {
  const daysOfWeek = ["8 am", "M", "T", "W", "R", "F"];

  const sectionColorMap = {};
  const initialTimeSlots = [];

  // Initialize time slots for each hour
  for (let hour = 9; hour <= 18; hour++) {
    const hour12 = hour > 12 ? hour - 12 : hour;
    const period = hour >= 12 ? "pm" : "am";
    const displayHour = hour12 === 0 ? 12 : hour12;
    initialTimeSlots.push({
      hour: displayHour,
      period: period,
      sections: new Array(5).fill(null),
    });
  }

  // Function to calculate position percentage based on start and end times
  const calculatePosition = (startTime, endTime) => {
    const [startHours, startMinutes] = startTime.split(":").map(Number);
    const [endHours, endMinutes] = endTime.split(":").map(Number);

    const topPercentage = (startMinutes / 60) * 100;
    const heightPercentage =
      (endHours - startHours) * 100 + ((endMinutes - startMinutes) * 100) / 60;

    return { topPercentage, heightPercentage };
  };

  // Process each section combination if combinations is defined
  if (combinations) {
    // Object to store section details (dept, course_code, section)
    const sectionDetails = {};

    // Fetch section details from combinations
    combinations.forEach((section) => {
      sectionDetails[section.id] = {
        dept: section.dept,
        course_code: section.course_code,
        section: section.section_id,
        location: section.classroom, // Added location
        alt_location: section.alternative_classroom, // Added alt_location
      };
    });

    combinations.forEach((section, index) => {
      const {
        id,
        days,
        start_time: startTime,
        end_time: endTime,
        alt_days: altDays,
        alt_start_time: altStartTime,
        alt_end_time: altEndTime,
      } = section;

      // Assign color to section ID
      if (!sectionColorMap[id]) {
        sectionColorMap[id] = colors[index % colors.length];
      }

      // Function to add section to time slot
      const addSectionToTimeSlot = (
        day,
        startTime,
        endTime,
        dept,
        course_code,
        section,
        location
      ) => {
        const column = daysOfWeek.indexOf(day) - 1;
        if (column !== -1) {
          const { topPercentage, heightPercentage } = calculatePosition(
            startTime,
            endTime
          );
          const sectionDiv = (
            <div
              key={`${id}-${day}`}
              className="absolute-position rounded"
              style={{
                top: `${topPercentage}%`,
                height: `${heightPercentage}%`,
                backgroundColor: sectionColorMap[id],
              }}
            >
              {`${dept} ${course_code} ${section}`} <br />
              {location} {/* Added location */}
            </div>
          );

          const hourIndex = Number(startTime.split(":")[0]) - 8;
          initialTimeSlots[hourIndex].sections[column] = sectionDiv;
        }
      };

      // Process main days
      days.forEach((day) => {
        addSectionToTimeSlot(
          day,
          startTime,
          endTime,
          sectionDetails[id].dept,
          sectionDetails[id].course_code,
          sectionDetails[id].section,
          sectionDetails[id].location // Use regular location
        );
      });

      // Process alternative days
      if (altDays && altStartTime && altEndTime) {
        altDays.forEach((altDay) => {
          addSectionToTimeSlot(
            altDay,
            altStartTime,
            altEndTime,
            sectionDetails[id].dept,
            sectionDetails[id].course_code,
            sectionDetails[id].section,
            sectionDetails[id].alt_location // Use alt_location
          );
        });
      }
    });
  }

  // Generate time slot elements
  const timeSlots = initialTimeSlots.map((slot, hourIndex) => (
    <tr key={hourIndex}>
      <td>
        {slot.hour} {slot.period}
      </td>
      {slot.sections.map((section, index) => (
        <td key={index} className="relative-position">
          {section}
        </td>
      ))}
    </tr>
  ));

  // Render the schedule table
  return (
    <table className="table table-bordered">
      <thead>
        <tr>
          {daysOfWeek.map((day, index) => (
            <th key={index}>{day}</th>
          ))}
        </tr>
      </thead>
      <tbody>{timeSlots}</tbody>
    </table>
  );
}

ScheduleTable.propTypes = {
  combinations: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      start_time: PropTypes.string.isRequired,
      end_time: PropTypes.string.isRequired,
      days: PropTypes.arrayOf(PropTypes.string).isRequired,
      alt_days: PropTypes.arrayOf(PropTypes.string), // Updated to allow alternative days
      alt_start_time: PropTypes.string, // Updated to allow alternative start time
      alt_end_time: PropTypes.string, // Updated to allow alternative end time
      dept: PropTypes.string.isRequired, // Add PropTypes for dept
      course_code: PropTypes.string.isRequired, // Add PropTypes for course_code
      section: PropTypes.string.isRequired, // Add PropTypes for section
      section_id: PropTypes.number.isRequired, // Add PropTypes for section_id
      classroom: PropTypes.string.isRequired, // Add PropTypes for classroom
      alternative_classroom: PropTypes.string, // Add PropTypes for alternative_classroom
    })
  ),
};

export default ScheduleTable;
