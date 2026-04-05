import React from "react";

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, info) {
    console.error("🔥 UI Crash:", error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={styles.container}>
          <h2>💥 Something broke</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={() => window.location.reload()}>
            🔄 Reload App
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

const styles = {
  container: {
    padding: "40px",
    textAlign: "center",
    color: "white",
    background: "#020617",
    minHeight: "100vh",
  },
};