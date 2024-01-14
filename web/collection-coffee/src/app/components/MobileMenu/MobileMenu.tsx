"use client";

import { ReactNode, useState } from "react";
import MenuIcon from "../../../../public/menuIcon.svg";
import ExitIcon from "../../../../public/exitIcon.svg";
import CollectionCoffeeLogo from "../../../../public/collectionCoffeeLogo.svg";
import "./mobile-menu.css";
import Link from "next/link";
import DiscordAltLogo from "../../../../public/discordAltLogo.svg";
import ThemeToggle from "../ThemeToggle/ThemeToggle";

type MobileMenuProps = {
  children: ReactNode;
};

const MobileMenu = ({ children }: MobileMenuProps) => {
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
          <div className="mobile-topnav-right-items">
            <Link href={`${process.env.DISCORD_INVITE_URL}`} target="_blank">
              <DiscordAltLogo className="discord-logo" />
            </Link>
            <ThemeToggle />
          </div>
          <button onClick={toggleMenu} className="mobile-topnav-button">
            {isOpen ? <ExitIcon /> : <MenuIcon />}
          </button>
        </div>
      </div>
      {isOpen ? <div className="mobile-topnav-open">{children}</div> : null}
    </div>
  );
};

export default MobileMenu;
