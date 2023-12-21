import LoginForm from "@/app/components/LoginForm/LoginForm";

export default function LoginPage({
  searchParams,
}: {
  searchParams: { message: string };
}) {
  return <LoginForm searchParams={searchParams} />;
}
