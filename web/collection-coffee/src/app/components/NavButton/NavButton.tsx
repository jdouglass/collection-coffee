import Link from "next/link";
import "./nav-button.css";

interface NavButtonProps {
  label: string;
  href: string;
  isActive: boolean;
}

export const NavButton = ({
  label,
  href,
  isActive,
  ...props
}: NavButtonProps) => {
  const activeMode = isActive ? "active" : "";

  return (
    <Link
      href={href}
      className={`${["nav-link", activeMode].join(" ")}`}
      {...props}
    >
      {label}
    </Link>
  );
};
