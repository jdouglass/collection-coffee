"use client";

import "./top-nav.css";
import CollectionCoffeeLogo from "../../../../public/collectionCoffeeLogo.svg";
import DiscordAltLogo from "../../../../public/discordAltLogo.svg";
import Link from "next/link";
import { NavButton } from "../NavButton/NavButton";
import { usePathname } from "next/navigation";
import ThemeToggle from "../ThemeToggle/ThemeToggle";

export const TopNav = () => {
  const pathname = usePathname();

  return (
    <div className="topnav-container">
      <div className="topnav-items">
        <div className="topnav-left">
          <Link href="/">
            <CollectionCoffeeLogo className="topnav-logo" />
          </Link>
          <div className="topnav-buttons">
            <NavButton
              label={"Collection"}
              href={"/"}
              isActive={pathname === "/"}
            />
            <NavButton
              label={"Contact"}
              href={"/contact"}
              isActive={pathname === "/contact"}
            />
          </div>
        </div>
        <div className="topnav-right">
          <Link href={`${process.env.DISCORD_INVITE_URL}`} target="_blank">
            <DiscordAltLogo className="discord-logo" />
          </Link>
          <ThemeToggle />
        </div>
      </div>
    </div>
  );
};
