export const Spinner = ({children}) => {
    return (
        <div className="flex items-center gap-2 text-gray-500 text-xl font-semibold">
        <span className="h-12 w-12 block rounded-full border-8 border-t-blue-darker animate-spin"></span>
        {children}
        </div>
    )
}