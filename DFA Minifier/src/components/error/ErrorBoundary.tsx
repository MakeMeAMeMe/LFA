// Global Imports
import React, { Component, ErrorInfo } from "react"

interface IErrorBoundaryState {
    hasError: boolean
}

interface IErrorBoundaryProps { }

class ErrorBoundary extends Component<IErrorBoundaryProps, IErrorBoundaryState> {
    constructor(props: IErrorBoundaryProps) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError(_: Error) {    // Update state so the next render will show the fallback UI.    
        return { hasError: true };
    }
    componentDidCatch(error: Error, errorInfo: ErrorInfo) {    // You can also log the error to an error reporting service    
        console.log(error, errorInfo);
    }
    render() {
        if (this.state.hasError) {      // You can render any custom fallback UI      
            return <h1>Something went wrong.</h1>;
        }
        return this.props.children;
    }
}
export default ErrorBoundary