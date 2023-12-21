import Link from "next/link";
import "./login-form.css";
import { redirect } from "next/navigation";
import { createClient } from "@/app/lib/utils/supabase/server";
import { cookies } from "next/headers";

export default function LoginForm({
  searchParams,
}: {
  searchParams: { message: string };
}) {
  const handleSignIn = async (formData: FormData) => {
    "use server";

    const email = formData.get("email") as string;
    const password = formData.get("password") as string;
    const cookieStore = cookies();
    const supabase = createClient(cookieStore);

    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) {
      return redirect("/account/login?message=Could not authenticate user");
    }

    return redirect("/");
  };

  return (
    <div className="auth-container">
      <div className="auth-container__title-section">
        <h2 className="auth-container__title">Sign in to your account</h2>
      </div>

      <div className="auth-container__form-section">
        <form className="auth-form" action={handleSignIn}>
          {/* Email Input */}
          <div className="auth-form__field">
            <label htmlFor="email" className="auth-form__label">
              Email address
            </label>
            <div className="auth-form__input-container">
              <input
                id="email"
                name="email"
                type="email"
                required
                className="auth-form__input"
              />
            </div>
          </div>

          {/* Password Input */}
          <div className="auth-form__field">
            <div className="auth-form__password-header">
              <label htmlFor="password" className="auth-form__label">
                Password
              </label>
              <div className="auth-form__forgot-password">
                <Link
                  href="/account/forgot-password"
                  className="auth-form__link"
                >
                  Forgot password?
                </Link>
              </div>
            </div>
            <div className="auth-form__input-container">
              <input
                id="password"
                name="password"
                type="password"
                required
                className="auth-form__input"
              />
            </div>
          </div>

          {/* Submit Button */}
          <div className="auth-form__submit-container">
            <button type="submit" className="auth-form__submit-button">
              Sign in
            </button>
          </div>
          {/* {loginError && (
            <p className="auth-form__error-text">Error: {loginError}</p>
          )} */}
          {searchParams?.message && (
            <p className="auth-form__error-text">{searchParams.message}</p>
          )}
        </form>

        <p className="auth-container__footer-text">
          Not a member?&nbsp;
          <Link href="/account/signup" className="auth-form__link">
            Sign up here
          </Link>
        </p>
      </div>
    </div>
  );
}
