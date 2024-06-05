import React from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";

const Nav = styled.nav`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 40px; // Increased padding for larger size
  background-color: #2c3e50;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const StyledLink = styled(Link)`
  color: white;
  text-decoration: none;
  margin-right: 20px;
  font-size: 32px; // Increased font size for better visibility
  &:hover {
    color: #18bc9c;
  }
`;

const ExternalLink = styled.a`
  color: white;
  text-decoration: none;
  margin-right: 20px;
  font-size: 32px; // Increased font size for better visibility
  &:hover {
    color: #e74c3c;
  }
`;

function NavBar() {
  return (
    <Nav>
      <div>
        <StyledLink to="/">Start Practicing</StyledLink>
        <ExternalLink
          href="/testCards"
          target="_blank"
          rel="noopener noreferrer"
        >
          Test Cards
        </ExternalLink>
      </div>
    </Nav>
  );
}

export default NavBar;
