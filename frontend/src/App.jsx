import React, { useState, useEffect } from "react";
import { createRoot } from "react-dom/client";
import ScheduleTable from "./components/ScheduleTable";
import Navbar from "./components/Navbar";
import CourseForm from "./components/CourseForm";
import Filters from "./components/Filters";
import CourseCard from "./components/CourseCard";
import CourseSectionCard from "./components/CourseSectionCard";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

function App() {
  const [selectedComponent, setSelectedComponent] = useState("Filters");
  const [coursesData, setCoursesData] = useState([]);
  const [selectedCourses, setSelectedCourses] = useState([]);
  const [sectionRoot, setSectionRoot] = useState(null);
  const [selectedCoursesData, setSelectedCoursesData] = useState([]);
  const [unselectedSectionKeys, setUnselectedSectionKeys] = useState([]);
  const [combinations, setCombinations] = useState([]);
  const [combinationIndex, setCombinationIndex] = useState(1); // Initial index is 1

  useEffect(() => {
    console.log("heh", selectedCoursesData);
  }, [selectedCoursesData]);

  useEffect(() => {
    const renderSections = () => {
      let root = sectionRoot;

      if (!root) {
        root = createRoot(document.getElementById("sectionContainer"));
        setSectionRoot(root);
      }

      root.render(
        <>
          {selectedCoursesData.map((courseData) => (
            <div className="col-12 py-1" key={courseData.id}>
              <CourseSectionCard
                key={courseData.id}
                course={courseData.course}
                sections={courseData.sections}
                onSectionClick={handleSectionClick}
              />
            </div>
          ))}
        </>
      );
    };

    renderSections();

    // Function to make the GET request
    const fetchData = async () => {
      try {
        // Make the GET request using the latest values of unselectedSectionKeys and selectedCourses
        const response = await axios.get(
          "http://localhost:8000/api/filter_sections/",
          {
            params: {
              unselectedKeys: unselectedSectionKeys,
              selectedCourseIds: selectedCoursesData.map(
                (courseData) => courseData.id
              ),
            },
          }
        );

        // Process the response data as needed
        console.log("GET request response:", response.data);

        // Update the combinations state with the new data
        setCombinations(response.data.combinations);
        // Reset the combination index to 1 whenever combinations are changed
        setCombinationIndex(1);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [selectedCoursesData, sectionRoot, unselectedSectionKeys]);

  const handleSelect = (componentName) => {
    setSelectedComponent(componentName);
  };

  const handleCoursesData = (data) => {
    console.log("Received data in App component:", data);
    if (data && data.courses) {
      setCoursesData(data.courses);
    } else {
      setCoursesData([]);
    }
  };

  const handleAddCourse = async (courseId) => {
    try {
      console.log("Course sent to backend for addition:", courseId);

      const isAlreadySelected = selectedCourses.includes(courseId);

      if (!isAlreadySelected) {
        setSelectedCourses([...selectedCourses, courseId]);
      }
    } catch (error) {
      console.error("Error sending course to backend for addition:", error);
    }
  };

  const handleRemoveCourse = (courseId) => {
    setSelectedCourses(selectedCourses.filter((id) => id !== courseId));
    setSelectedCoursesData(
      selectedCoursesData.filter((course) => course.id !== courseId)
    );
  };

  const handleCourseDataReceived = (courseData) => {
    console.log("Received course data in App component:", courseData);

    const { courseData: course, sectionsData: sections } = courseData;
    setSelectedCoursesData([
      ...selectedCoursesData,
      { id: course.id, course, sections },
    ]);
  };

  const handleSectionClick = (sectionKey, isSelected) => {
    console.log(isSelected);
    if (isSelected) {
      setUnselectedSectionKeys((prevKeys) =>
        prevKeys.filter((key) => key !== sectionKey)
      );
    } else {
      setUnselectedSectionKeys((prevKeys) => [...prevKeys, sectionKey]);
    }
  };

  const handleBackClick = () => {
    // Decrease the combination index by 1, ensuring it doesn't go below 1
    setCombinationIndex((prevIndex) => Math.max(prevIndex - 1, 1));
  };

  const handleForwardClick = () => {
    // Increase the combination index by 1, ensuring it doesn't exceed the length of combinations
    setCombinationIndex((prevIndex) =>
      Math.min(prevIndex + 1, combinations.length)
    );
  };

  return (
    <React.Fragment>
      <Navbar />
      <div className="container-fluid py-4">
        <div className="row" id="mainRow">
          <div className="col-4 px-5">
            <div className="container" id="selContainer">
              <div className="row" id="selDiv">
                <Filters
                  selectedComponent={selectedComponent}
                  handleSelect={handleSelect}
                />
              </div>

              <div className="overflow-container">
                <div className="row">
                  {selectedComponent === "Filters" && (
                    <div className="col-12 pt-3" id="sectionContainer"></div>
                  )}
                </div>
                {selectedComponent === "Filters" && (
                  <div className="row">
                    <div className="col-12 text-center pt-3 m-0">
                      <CourseForm handleCoursesData={handleCoursesData} />
                    </div>
                  </div>
                )}
                {selectedComponent === "Filters" && (
                  <div className="row pt-3" id="selComps">
                    {coursesData.map((course) => (
                      <div className="col-12 py-1" key={course.id}>
                        <CourseCard
                          course={course}
                          handleAddCourse={handleAddCourse}
                          handleRemoveCourse={handleRemoveCourse}
                          isSelected={selectedCourses.includes(course.id)}
                          onCourseDataReceived={handleCourseDataReceived}
                        />
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
          <div className="col-8 px-5">
            <div className="d-flex justify-content-center align-items-center">
              <button
                className="btn btn-dark"
                onClick={handleBackClick}
                disabled={combinationIndex === 1}
              >
                &lt;
              </button>
              <span className="mx-2">
                {combinations.length > 0
                  ? `Combination ${combinationIndex} of ${combinations.length}`
                  : "No combinations available"}
              </span>
              <button
                className="btn btn-dark"
                onClick={handleForwardClick}
                disabled={combinationIndex === combinations.length}
              >
                &gt;
              </button>
            </div>
            <ScheduleTable combinations={combinations[combinationIndex - 1]} />
          </div>
        </div>
      </div>
    </React.Fragment>
  );
}

export default App;
