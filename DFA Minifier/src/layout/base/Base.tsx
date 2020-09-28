import React, { Component, Fragment } from "react"
import Container from "react-bootstrap/Container"

class Base extends Component {
    render() {
        return (
            <Fragment>
                <header>
                    <Container fluid>

                    <h3>
                        Minimizador AFD
                    </h3>
                    </Container>
                </header>
                <section id="content">
                    <Container fluid>
                        {this.props.children}
                    </Container>
                </section>
            </Fragment>
        )
    }
}

export default Base;
