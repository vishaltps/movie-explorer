import { formatDate } from '../../../shared/lib/formatters';
import { RatingStars } from '../../../shared/components/RatingStars';
import type { ReviewRead } from '../../../shared/types';

type ReviewListProps = {
  reviews: ReviewRead[];
};

export function ReviewList({ reviews }: ReviewListProps) {
  if (reviews.length === 0) {
    return (
      <p className="text-[color:var(--muted)]">
        No reviews yet for this movie.
      </p>
    );
  }

  return (
    <div className="space-y-4">
      {reviews.map((review) => (
        <article
          key={review.id}
          className="rounded-[1.5rem] border border-[color:var(--border)] bg-white/60 p-4"
        >
          <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h4 className="font-semibold">{review.author_name}</h4>
              <p className="text-sm text-[color:var(--muted)]">
                {formatDate(review.created_at)}
              </p>
            </div>
            <RatingStars rating={review.rating} />
          </div>
          <p className="mt-3 text-[color:var(--text)]">{review.comment}</p>
        </article>
      ))}
    </div>
  );
}
