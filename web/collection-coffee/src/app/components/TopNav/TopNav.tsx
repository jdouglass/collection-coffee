import "./top-nav.css";
import CollectionCoffeeLogo from "../../../../public/collectionCoffeeLogo.svg";
import DiscordAltLogo from "../../../../public/discordAltLogo.svg";
import Link from "next/link";
import ThemeToggle from "../ThemeToggle/ThemeToggle";
import { cookies } from "next/headers";
import { createClient } from "@/app/lib/utils/supabase/server";
import AuthButton from "../AuthButton/AuthButton";

export const TopNav = () => {
  const cookieStore = cookies();

  const canInitSupabaseClient = () => {
    try {
      createClient(cookieStore);
      return true;
    } catch (e) {
      return false;
    }
  };

  const isSupabaseConnected = canInitSupabaseClient();

  return (
    <div className="topnav-container">
      <div className="topnav-items">
        <div className="topnav-left">
          <Link href="/">
            <CollectionCoffeeLogo className="topnav-logo" />
          </Link>
        </div>
        <div className="topnav-right">
          <Link href={`${process.env.DISCORD_INVITE_URL}`} target="_blank">
            <DiscordAltLogo className="discord-logo" />
          </Link>
          <ThemeToggle />
          {isSupabaseConnected && <AuthButton />}
        </div>
      </div>
    </div>
  );
};
