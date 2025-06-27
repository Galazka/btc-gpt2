export function Button({ children, onClick, disabled, variant }) {
  const baseStyle = `px-4 py-2 rounded font-medium transition ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`;
  const variantStyle = variant === 'outline'
    ? 'border border-white text-white bg-transparent hover:bg-white hover:text-black'
    : 'bg-yellow-500 text-black hover:bg-yellow-600';

  return (
    <button onClick={onClick} disabled={disabled} className={`${baseStyle} ${variantStyle}`}>
      {children}
    </button>
  );
}