import { createClient } from "@/app/lib/utils/supabase/server";
import Link from "next/link";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import "./mobile-auth-button.css";
import { MobileLogoutButton } from "../MobileLogoutButton/MobileLogoutButton";

export default async function MobileAuthButton() {
  const cookieStore = cookies();
  const supabase = createClient(cookieStore);

  const {
    data: { user },
  } = await supabase.auth.getUser();

  const signOut = async () => {
    "use server";

    const cookieStore = cookies();
    const supabase = createClient(cookieStore);
    await supabase.auth.signOut();
    return redirect("/");
  };

  return user ? (
    <div>
      <form action={signOut}>
        <MobileLogoutButton />
      </form>
    </div>
  ) : (
    <div className="mobile-auth__button--container">
      <Link
        href="/account/login"
        className="mobile-auth__button mobile-sign-in__button mobile-auth-button"
      >
        Sign in
      </Link>
      <Link
        href="/account/signup"
        className="mobile-auth__button mobile-sign-up__button mobile-auth-button"
      >
        Sign up
      </Link>
    </div>
  );
}
