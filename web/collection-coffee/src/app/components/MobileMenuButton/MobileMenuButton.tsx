"use client";

import { useState } from "react";
import MenuIcon from "../../../../public/menuIcon.svg";
import ExitIcon from "../../../../public/exitIcon.svg";
import CollectionCoffeeLogo from "../../../../public/collectionCoffeeLogo.svg";
import "./mobile-menu-button.css";
import Link from "next/link";
import AuthButton from "../AuthButton/AuthButton";

type MobileMenuProps = {
  isSupabaseConnected: boolean;
};

const MobileMenu = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="mobile-topnav">
      <div className="mobile-topnav-items">
        <div className="mobile-topnav-left">
          <Link href="/">
            <CollectionCoffeeLogo className="mobile-topnav-logo" />
          </Link>
        </div>
        <div className="mobile-topnav-right">
          <button onClick={toggleMenu}>
            {isOpen ? <ExitIcon /> : <MenuIcon />}
          </button>
        </div>
      </div>
      {/* {isOpen ? <div>{isSupabaseConnected && <AuthButton />}</div> : null} */}
    </div>
  );
};

export default MobileMenu;
