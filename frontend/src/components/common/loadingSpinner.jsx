import '../../styles/components/LoadingSpinner.css';


const LoadingSpinner = ({ size = 'md' }) => {
  return (
    <div className="loading-container">
      <div className={`loading-spinner ${size}`}></div>
    </div>
  );
};

export default LoadingSpinner;