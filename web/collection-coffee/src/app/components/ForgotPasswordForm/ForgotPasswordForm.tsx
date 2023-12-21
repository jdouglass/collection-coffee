import "./forgot-password-form.css";
import { redirect } from "next/navigation";
import { createClient } from "@/app/lib/utils/supabase/server";
import { cookies, headers } from "next/headers";

export default function ForgotPasswordForm({
  searchParams,
}: {
  searchParams: { message: string };
}) {
  const handlePasswordReset = async (formData: FormData) => {
    "use server";

    const origin = headers().get("origin");
    const email = formData.get("email") as string;
    const cookieStore = cookies();
    const supabase = createClient(cookieStore);

    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${origin}/auth/callback?token=/account/update-password`,
    });

    if (error) {
      return redirect("/account/forgot-password?message=Error occurred");
    }

    return redirect(
      "/account/forgot-password?message=Check your email to finish resetting your password"
    );
  };

  return (
    <div className="auth-container">
      <div className="auth-container__title-section">
        <h2 className="auth-container__title">Reset your password</h2>
      </div>

      <div className="auth-container__form-section">
        <form className="auth-form" action={handlePasswordReset}>
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

          {/* Submit Button */}
          <div className="auth-form__submit-container">
            <button type="submit" className="auth-form__submit-button">
              Reset Password
            </button>
          </div>
          {/* {loginError && (
            <p className="auth-form__error-text">Error: {loginError}</p>
          )} */}
          {searchParams?.message && (
            <p className="auth-form__error-text">{searchParams.message}</p>
          )}
        </form>
      </div>
    </div>
  );
}
